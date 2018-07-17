"""
Python GIT tool to check pending changes and get last commit info

``gitchecker.check_status_and_get_commit_info()`` checks if there is
any pending changes in GIT repository status and returns the last commit info:
    - sha (string): commit SHA (7 digits length)
    - author (string): author name
    - authored_datetime (datetime): author datetime
    - committer (string): committer name
    - committed_datetime (datetime): committer datetime
By default it raises an ``Exception`` if there are any pending changes but
it can be configured to only show a warning instead.
"""

import re
from collections import namedtuple
from git import Repo  # http://gitpython.readthedocs.io/


def check_status_and_get_commit_info(repo_path="",
                                     warning_instead_of_error=False,
                                     ignore_untracked_files=False,
                                     ignore_files_regex=None,
                                     logger=None):

    """checks if there is any pending changes in GIT
    repository status and returns the last commit info

    Args:
        repo_path (string): GIT repository path.
        warning_instead_of_error (bool): By default an ``Exception`` is raised
            if there are any pending changes unless this param is truthy
        ignore_untracked_files (bool): If ``True``, untracked files will be
            ignored completely, not raising errors and not showing warnings.
        ignore_files_regex (string): Files will be ignored if its path matches
            the regex pattern.
        logger: If a ``logger`` is provided, it will be used only if it
            has an ``error()`` or ``warning()`` method. The required
            method depends on the value of ``warning_instead_of_error``.
            If no ``logger`` provided or no proper log function exists
            in ``logger`` , ``print()`` will be used instead.
    Returns:
        (CommitInfo) Last commit info in a namedtuple format:
            - sha (string): commit SHA (7 digits length)
            - author (string): author name
            - authored_datetime (datetime): author datetime
            - committer (string): committer name
            - committed_datetime (datetime): committer datetime
    """

    git_status = _get_git_status(repo_path, ignore_files_regex, ignore_untracked_files)

    if git_status.total_changes:
        status_msg = _get_status_msg(git_status)
        if warning_instead_of_error:
            _log_warning(status_msg, logger)
        else:
            _log_and_raise_error(status_msg, logger)

    return git_status.commit_info


GitStatus = namedtuple("GitStatus", ["commit_info",
                                     "staged_files",
                                     "unstaged_files",
                                     "untracked_files",
                                     "total_changes"])

CommitInfo = namedtuple("CommitInfo", ["sha",
                                       "author",
                                       "authored_datetime",
                                       "committer",
                                       "committed_datetime"])


def _get_git_status(repo_path="", ignore_files_regex=None, ignore_untracked_files=False):
    repo = Repo(repo_path)

    last_commit     = repo.head.commit
    commit_info     = CommitInfo(repo.git.rev_parse(last_commit.hexsha, short=7),
                                 last_commit.author.name,
                                 last_commit.authored_datetime,
                                 last_commit.committer.name,
                                 last_commit.committed_datetime)

    filter_diff_fn  = lambda df: __filter_diff_file(df, ignore_files_regex)
    staged_files    = __filter_diff(repo.index.diff("HEAD"), filter_diff_fn)
    unstaged_files  = __filter_diff(repo.index.diff(None), filter_diff_fn)

    filter_files_fn = lambda df: __filter_filename(df, ignore_files_regex)
    untracked_files = __filter_diff(repo.untracked_files, filter_files_fn)

    total_changes = staged_files + unstaged_files

    if not ignore_untracked_files:
        total_changes += untracked_files

    return GitStatus(commit_info,
                     staged_files,
                     unstaged_files,
                     untracked_files,
                     total_changes)


def __filter_diff(diff, filter_diff_fn):
    return len(list(filter(filter_diff_fn, list(diff))))


def __filter_diff_file(diff_file, ignore_files_regex=None):
    return (__filter_filename(diff_file.a_path, ignore_files_regex) and
            __filter_filename(diff_file.b_path, ignore_files_regex))


def __filter_filename(filename, ignore_files_regex=None):
    return (not ignore_files_regex or
            not filename or
            not re.match(ignore_files_regex, filename))


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
