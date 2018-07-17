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
            gitchecker.check_status_and_get_commit_info(self.repo_path)
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
        commit_info = "foo-value"
        expected_total_changes = self._get_total_changes(test_config.expected_results)
        expected_commit_info = self._get_expected_commit_info(is_warning, expected_total_changes)

        # act
        commit_info, exception = self._act(is_warning, expected_total_changes, test_config)

        # assert
        if expected_commit_info:
            assert expected_commit_info.sha == commit_info.sha
        else:
            assert None is commit_info

        self._assert(test_config.expected_results,
                     expected_total_changes,
                     exception,
                     print_mock,
                     is_warning)

        # teardown
        test_config.teardown(self, test_config_state)

    def _get_expected_commit_info(self, is_warning, expected_total_changes):
        if is_warning or not expected_total_changes:
            return gitchecker.CommitInfo(self.repo.head.commit.hexsha[:7],
                                         None,
                                         None,
                                         None,
                                         None)

        return None

    def _act(self, is_warning, expected_total_changes, test_config):
        ignore_untracked_files = test_config.ignore_untracked_files
        ignore_files_regex = test_config.ignore_files_regex
        warning_instead_of_error = is_warning

        if is_warning or not expected_total_changes:
            commit_info =\
                gitchecker.check_status_and_get_commit_info(self.repo_path,
                                                            warning_instead_of_error,
                                                            ignore_untracked_files,
                                                            ignore_files_regex)

            return commit_info, None

        with pytest.raises(Exception) as ex:
            commit_info =\
                gitchecker.check_status_and_get_commit_info(self.repo_path,
                                                            warning_instead_of_error,
                                                            ignore_untracked_files,
                                                            ignore_files_regex)

            return commit_info, None

        return None, ex

    def _assert(self, expected_results, expected_total_changes, exception, print_mock, is_warning):
        if expected_total_changes:
            expected_print_msg, expected_ex_msg = self._get_msgs(expected_results, is_warning)
            print_mock.assert_called_once_with(expected_print_msg)
            if is_warning:
                assert exception is None
            else:
                assert expected_ex_msg == str(exception.value)

        else:
            print_mock.assert_not_called()
            assert exception is None

    @classmethod
    def _get_total_changes(cls, expected_results):
        return (expected_results.staged_files +
                expected_results.unstaged_files +
                expected_results.untracked_files)

    @classmethod
    def _create_foo_file(cls, filename=None):
        if not filename:
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
