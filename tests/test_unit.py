from unittest.mock import call, MagicMock, patch
import pytest

from gitchecker import gitchecker


def _get_git_status(commit_info="foo-commit-info",
                    staged_files="foo-staged-files",
                    unstaged_files="foo-unstaged-files",
                    untracked_files="foo-untracked-files",
                    total_changes=0):

    return gitchecker.GitStatus(commit_info,
                                staged_files,
                                unstaged_files,
                                untracked_files,
                                total_changes)


@patch("gitchecker.gitchecker._log_warning")
@patch("gitchecker.gitchecker._log_and_raise_error")
@patch("gitchecker.gitchecker._get_status_msg")
@patch("gitchecker.gitchecker._get_git_status")
class TestUnitGitChecker_CheckCleanStatus:

    foo_commit_info = "foo-commit-info"
    foo_repo_path = "foo/repo/path"
    foo_wioe = "foo-warning-instead-of-error"
    foo_iuf = "foo-ignore-untracked-files"
    foo_ifr = None
    foo_logger = "foo-logger"

    def test_when_no_changes(self,
                             _get_git_status_mock,
                             _get_status_msg_mock,
                             _log_and_raise_error_mock,
                             _log_warning_mock):
        # arrange
        _get_git_status_mock.return_value = _get_git_status(self.foo_commit_info)

        # act
        commit_info = gitchecker.check_status_and_get_commit_info(self.foo_repo_path,
                                                                  self.foo_wioe,
                                                                  self.foo_iuf,
                                                                  self.foo_ifr,
                                                                  self.foo_logger)

        # assert
        assert commit_info is self.foo_commit_info
        _get_git_status_mock.assert_called_once_with(self.foo_repo_path, self.foo_ifr, self.foo_iuf)
        _get_status_msg_mock.assert_not_called()
        _log_and_raise_error_mock.assert_not_called()
        _log_warning_mock.assert_not_called()

    def test_when_changes_and_warning(self,
                                      _get_git_status_mock,
                                      _get_status_msg_mock,
                                      _log_and_raise_error_mock,
                                      _log_warning_mock):
        # arrange
        foo_git_status = _get_git_status(self.foo_commit_info, total_changes=1)
        _get_git_status_mock.return_value = foo_git_status
        foo_status_msg = "foo-status-msg"
        _get_status_msg_mock.return_value = foo_status_msg

        # act
        commit_info = gitchecker.check_status_and_get_commit_info(self.foo_repo_path,
                                                                  True,
                                                                  self.foo_iuf,
                                                                  self.foo_ifr,
                                                                  self.foo_logger)

        # assert
        assert self.foo_commit_info is commit_info
        _get_git_status_mock.assert_called_once_with(self.foo_repo_path, self.foo_ifr, self.foo_iuf)
        _get_status_msg_mock.assert_called_once_with(foo_git_status)
        _log_and_raise_error_mock.assert_not_called()
        _log_warning_mock.assert_called_once_with(foo_status_msg, self.foo_logger)

    def test_when_changes_and_error(self,
                                    _get_git_status_mock,
                                    _get_status_msg_mock,
                                    _log_and_raise_error_mock,
                                    _log_warning_mock):
        # arrange
        foo_git_status = _get_git_status(self.foo_commit_info, total_changes=1)
        _get_git_status_mock.return_value = foo_git_status
        foo_status_msg = "foo-status-msg"
        _get_status_msg_mock.return_value = foo_status_msg

        # act
        commit_info = gitchecker.check_status_and_get_commit_info(self.foo_repo_path,
                                                                  False,
                                                                  self.foo_iuf,
                                                                  self.foo_ifr,
                                                                  self.foo_logger)

        # assert
        assert self.foo_commit_info is commit_info
        _get_git_status_mock.assert_called_once_with(self.foo_repo_path, self.foo_ifr, self.foo_iuf)
        _get_status_msg_mock.assert_called_once_with(foo_git_status)
        _log_and_raise_error_mock.assert_called_once_with(foo_status_msg, self.foo_logger)
        _log_warning_mock.assert_not_called()


def _get_diff_file_mock(file_type, i):
    diff_file_mock = MagicMock()
    diff_file_mock.a_path = _get_foo_filename(file_type, i)
    diff_file_mock.b_path = _get_foo_filename(file_type, i)

    return diff_file_mock


def _get_foo_filename(file_type, i):
    return "foo-{}/file-{}.py".format(file_type, i)


@patch.object(gitchecker, "Repo")
class TestUnitGitChecker_GetGitStatus:

    foo_commit_sha = "f00c0mm1t"
    foo_repo_path = "foo/repo/path"
    foo_staged_file = MagicMock()

    foo_staged_files    = [_get_diff_file_mock("staged", i) for i in range(3)]
    foo_unstaged_files  = [_get_diff_file_mock("unstaged", i) for i in range(5)]
    foo_untracked_files = [_get_foo_filename("untracked", i) for i in range(7)]

    def test_not_ignoring(self, RepoMock):
        # arrange
        repo_mock = self._arrange_repo_mock(RepoMock)
        foo_commit_info = self._arrange_foo_commit_info(repo_mock)

        # act
        git_status = gitchecker._get_git_status(self.foo_repo_path)

        # assert
        expected_total_changes = 15
        self._assert(RepoMock, repo_mock, git_status, foo_commit_info, expected_total_changes)

    def test_ignoring_untracked_files(self, RepoMock):
        # arrange
        repo_mock = self._arrange_repo_mock(RepoMock)
        foo_commit_info = self._arrange_foo_commit_info(repo_mock)

        # act
        git_status = gitchecker._get_git_status(self.foo_repo_path, ignore_untracked_files=True)

        # assert
        expected_total_changes = 8
        self._assert(RepoMock, repo_mock, git_status, foo_commit_info, expected_total_changes)

    def test_ignoring_files_regex(self, RepoMock):
        # arrange
        ignore_files_regex = "^foo-(staged|unstaged|untracked)\/file-[23]\.py$"
        repo_mock = self._arrange_repo_mock(RepoMock)
        foo_commit_info = self._arrange_foo_commit_info(repo_mock)

        # act
        git_status = gitchecker._get_git_status(self.foo_repo_path,
                                                ignore_files_regex=ignore_files_regex)

        # assert
        expected_git_status = _get_git_status(foo_commit_info, 2, 3, 5, 10)
        self._assert(RepoMock,
                     repo_mock,
                     git_status,
                     foo_commit_info,
                     expected_git_status=expected_git_status)

    def _arrange_repo_mock(self, RepoMock):
        repo_mock = RepoMock.return_value
        repo_mock.index.diff.side_effect = [
            self.foo_staged_files, self.foo_unstaged_files
        ]
        repo_mock.untracked_files = self.foo_untracked_files
        repo_mock.git.rev_parse.return_value = self.foo_commit_sha

        return repo_mock

    def _arrange_foo_commit_info(self, repo_mock):
        last_commit_mock = repo_mock.head.commit

        return gitchecker.CommitInfo(self.foo_commit_sha,
                                     last_commit_mock.author.name,
                                     last_commit_mock.authored_datetime,
                                     last_commit_mock.committer.name,
                                     last_commit_mock.committed_datetime)

    def _assert(self,
                RepoMock,
                repo_mock,
                git_status,
                foo_commit_info,
                expected_total_changes=None,
                expected_git_status=None):

        RepoMock.assert_called_once_with(self.foo_repo_path)

        if not expected_git_status:
            expected_git_status = \
                _get_git_status(foo_commit_info, 3, 5, 7, expected_total_changes)

        assert expected_git_status == git_status
        expected_diff_calls = [call("HEAD"), call(None)]
        repo_mock.index.diff.assert_has_calls(expected_diff_calls)


class TestUnitGitChecker_GetStatusMsg:

    def test(self):
        # arrange
        foo_git_status = _get_git_status()
        original_tmpl = gitchecker.STATUS_MSG_TMPL
        gitchecker.STATUS_MSG_TMPL = "Foo1: {} Foo2: {} Foo3: {}"

        # act
        msg = gitchecker._get_status_msg(foo_git_status)

        # assert
        expected_msg = "Foo1: foo-staged-files Foo2: foo-unstaged-files Foo3: foo-untracked-files"
        assert expected_msg == msg
        gitchecker.STATUS_MSG_TMPL = original_tmpl


class TestUnitGitChecker_LogAndRaiseError:

    foo_msg = "foo-msg"

    def test_error_logger(self):
        # arrange
        logger_mock = MagicMock()

        # act
        with pytest.raises(Exception) as ex:
            gitchecker._log_and_raise_error(self.foo_msg, logger=logger_mock)

        # assert
        assert "ERROR: foo-msg" == str(ex.value)
        logger_mock.error.asser_has_been_called_once_with("foo-msg")

    @patch("gitchecker.gitchecker.print")
    def test_print(self, print_mock):
        # arrange

        # act
        with pytest.raises(Exception) as ex:
            gitchecker._log_and_raise_error(self.foo_msg)

        # assert
        expected_error_msg = "ERROR: foo-msg"
        assert expected_error_msg == str(ex.value)
        sep_msg = "*" * (2 + len(expected_error_msg))
        expected_print_msg = sep_msg + "\n " + expected_error_msg + "\n" + sep_msg
        print_mock.assert_called_once_with(expected_print_msg)


class TestUnitGitChecker_Log:

    foo_msg = "foo-msg"

    def test_logger(self):
        # arrange
        logger_mock = MagicMock()

        # act
        gitchecker._log_warning(self.foo_msg, logger_mock)

        # assert
        logger_mock.warning.assert_called_once_with(self.foo_msg)

    @patch("gitchecker.gitchecker.print")
    def test_print(self, print_mock):
        # arrange

        # act
        gitchecker._log_warning(self.foo_msg)

        # assert
        expected_warning_msg = " WARNING: foo-msg"
        sep_msg = "*" * (1 + len(expected_warning_msg))
        expected_print_msg = sep_msg + "\n" + expected_warning_msg + "\n" + sep_msg
        print_mock.assert_called_once_with(expected_print_msg)
