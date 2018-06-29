"""
Python GIT tool to check pending changes

``gitchecker.check_clean_status()`` checks if there is any pending changes
in GIT repository status and returns the last commit SHA (7 digits length).
By default it raises an ``Exception`` if there are any pending changes but
it can be configured to only show a warning instead.
"""

from collections import namedtuple
from git import Repo  # http://gitpython.readthedocs.io/


def check_clean_status(repo_path="",
                       warning_instead_of_error=False,
                       ignore_untracked_files=False,
                       logger=None):

    """checks if there is any pending changes in GIT repository status
    and returns the last commit SHA (7 digits length)

    Args:
        repo_path (string): GIT repository path.
        warning_instead_of_error (bool): By default ``check_clean_status``
            raises an ``Exception`` if there are any pending changes unless
        ignore_untracked_files (bool): If ``True``, untracked files will be
            ignored completely, not raising errors and not showing warnings.
        logger: If a ``logger`` is provided, it will be used only if it
            has an ``error()`` or ``warning()`` method. The required
            method depends on the value of ``warning_instead_of_error``.
            If no ``logger`` provided or no proper log function exists
            in ``logger`` , ``print()`` will be used instead.
    Returns:
        string: Last commit SHA (7 digits length).
    """

    git_status = _get_git_status(repo_path, ignore_untracked_files)

    if git_status.total_changes:
        status_msg = _get_status_msg(git_status)
        if warning_instead_of_error:
            _log_warning(status_msg, logger)
        else:
            _log_and_raise_error(status_msg, logger)

    return git_status.commit_sha


GitStatus = namedtuple("GitStatus", ["commit_sha",
                                     "staged_files",
                                     "unstaged_files",
                                     "untracked_files",
                                     "total_changes"])


def _get_git_status(repo_path="", ignore_untracked_files=False):
    repo = Repo(repo_path)

    commit_sha = repo.git.rev_parse(repo.head.commit.hexsha, short=7)
    staged_files    = len(repo.index.diff("HEAD"))
    unstaged_files  = len(repo.index.diff(None))
    untracked_files = len(repo.untracked_files)

    total_changes = staged_files + unstaged_files

    if not ignore_untracked_files:
        total_changes += untracked_files

    return GitStatus(commit_sha,
                     staged_files,
                     unstaged_files,
                     untracked_files,
                     total_changes)


STATUS_MSG_TMPL = "There are " +\
                  "{} staged file(s), " +\
                  "{} unstaged file(s) and " +\
                  "{} untracked file(s)"


def _get_status_msg(git_status):
    return STATUS_MSG_TMPL.format(git_status.staged_files,
                                  git_status.unstaged_files,
                                  git_status.untracked_files)


def _log_and_raise_error(msg, logger=None):
    if logger and hasattr(logger, "error") and callable(logger.error):
        logger.error(msg)
    else:
        sep_msg = "*" * (9 + len(msg))
        print("{}\n ERROR: {}\n{}".format(sep_msg, msg, sep_msg))

    raise Exception("ERROR: {}".format(msg))


def _log_warning(msg, logger=None):
    if logger and hasattr(logger, "warning") and callable(logger.warning):
        logger.warning(msg)
    else:
        sep_msg = "*" * (11 + len(msg))
        print("{}\n WARNING: {}\n{}".format(sep_msg, msg, sep_msg))
