import itertools
import os
from time import time
from unittest.mock import patch
from git import Actor, Repo
import pytest

from gitchecker import gitchecker
from tests.functional_config import FuncTestConfig, test_configs


error_warning_params = [True, False]
functional_test_params = itertools.product(test_configs, error_warning_params)


def get_test_param_id(param):
    if isinstance(param, FuncTestConfig):
        return param.id

    return "WARN" if param else "ERROR"


@patch("gitchecker.gitchecker.print")
class TestFunctionalGitChecker:

    repo_path = ""
    author    = Actor("Test Actor", "author@test.com")
    committer = Actor("Test Committer", "committer@test.com")

    def setup_method(self):
        self.repo = Repo(self.repo_path)

        try:
            gitchecker.check_clean_status(self.repo_path)
        except Exception:
            raise Exception("TestFunctionalGitChecker: " +
                            "git status should be clean before executing functional testing")
            # # for development: comment previous exception raising and use the following:
            # self.repo.git.add(u=True)
            # self._commit("auto-commit: functional testing development")

    @pytest.mark.parametrize("test_config,is_warning",
                             functional_test_params,
                             ids=get_test_param_id)
    def test_run(self, print_mock, test_config, is_warning):
        # test setup
        test_config_state = test_config.setup(self)

        # arrange
        commit_sha = "foo-value"
        expected_commit_sha = self._get_expected_commit_sha(is_warning)

        # act
        commit_sha, exception = self._act(is_warning)

        # test teardown
        assert expected_commit_sha == commit_sha
        self._assert_warning_or_error(test_config.expected_results,
                                      exception,
                                      print_mock,
                                      is_warning)

        # teardown
        test_config.teardown(self, test_config_state)

    def _get_expected_commit_sha(self, is_warning):
        if is_warning:
            return self.repo.head.commit.hexsha[:7]

        return None

    def _act(self, is_warning):
        if is_warning:
            commit_sha =\
                gitchecker.check_clean_status(self.repo_path, warning_instead_of_error=True)

            return commit_sha, None

        with pytest.raises(Exception) as ex:
            commit_sha = gitchecker.check_clean_status(self.repo_path)

            return commit_sha, None

        return None, ex

    def _assert_warning_or_error(self, expected_results, exception, print_mock, is_warning):
        expected_print_msg, expected_ex_msg = self._get_msgs(expected_results, is_warning)
        print_mock.assert_called_once_with(expected_print_msg)
        if is_warning:
            assert exception is None
        else:
            assert expected_ex_msg == str(exception.value)

    @classmethod
    def _create_foo_file(cls):
        filename = "{}.txt".format(str(time() * 1000))
        cls._write_file(filename, "foo")

        return filename

    @classmethod
    def _modify_file(cls, filename):
        cls._write_file(filename, "more-foo")

    @classmethod
    def _write_file(cls, filename, content):
        with open(os.path.join(cls.repo_path, filename), "w") as my_file:
            my_file.write("{}\n".format(content))

    @classmethod
    def _remove_file(cls, filename):
        os.remove(os.path.join(cls.repo_path, filename))

    @classmethod
    def _get_msgs(cls, expected_results, is_warning=False):
        ex_msg = ""
        print_msg = \
            "There are {} staged file(s), {} unstaged file(s) and {} untracked file(s)"\
            .format(expected_results.staged_files,
                    expected_results.unstaged_files,
                    expected_results.untracked_files)

        if is_warning:
            print_msg = " WARNING: {}".format(print_msg)
        else:
            ex_msg = "ERROR: {}".format(print_msg)
            print_msg = " {}".format(ex_msg)

        sep_msg = "*" * (1 + len(print_msg))
        print_msg = sep_msg + "\n" + print_msg + "\n" + sep_msg

        return print_msg, ex_msg

    def _stage(self, filename):
        self.repo.index.add([filename])

    def _stage_all(self):
        self.repo.git.add(update=True)

    def _unstage(self, filename):
        self.repo.index.remove([filename])

    def _commit(self, commit_msg):
        self.repo.index.commit(commit_msg, author=self.author, committer=self.committer)
