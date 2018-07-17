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

from gitchecker.gitchecker import check_status_and_get_commit_info
