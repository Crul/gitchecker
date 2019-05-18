fkjsdfjsjfks




jkfsjklfsjk


[![Travis build](https://travis-ci.org/Crul/gitchecker.svg?branch=master)](https://travis-ci.org/Crul/gitchecker) 
[![Coverage Status](https://coveralls.io/repos/github/Crul/gitchecker/badge.svg?branch=master)](https://coveralls.io/github/Crul/gitchecker?branch=master)
[![pypi-version](https://img.shields.io/pypi/v/gitchecker.svg)](https://pypi.org/project/gitchecker/)
[![pypi-wheel](https://img.shields.io/pypi/wheel/gitchecker.svg)](https://pypi.org/project/gitchecker/)
[![pypi-format](https://img.shields.io/pypi/format/gitchecker.svg)](https://pypi.org/project/gitchecker/)
[![pypi-pyversions](https://img.shields.io/pypi/pyversions/gitchecker.svg)](https://pypi.org/project/gitchecker/)
[![pypi-implementation](https://img.shields.io/pypi/implementation/gitchecker.svg)](https://pypi.org/project/gitchecker/)
[![pypi-status](https://img.shields.io/pypi/status/gitchecker.svg)](https://pypi.org/project/gitchecker/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/db52183d1abe4ae389fddbf9911c83b2)](https://www.codacy.com/app/Crul/gitchecker)
# Python GIT tool to check pending changes and get last commit info 

``gitchecker.check_status_and_get_commit_info()`` checks if there is
any pending changes in GIT repository status and returns the last commit info:

- sha (string): commit SHA (7 digits length)
- author (string): author name
- authored_datetime (datetime): author datetime
- committer (string): committer name
- committed_datetime (datetime): committer datetime

By default it raises an ``Exception`` if there are any pending changes but
it can be configured to only show a warning instead.

## Requirements

- Python 3.5 or newer
- Git 1.7.0 or newer, because [gitpython dependency](https://gitpython.readthedocs.io/en/stable/intro.html#requirements)

## Install

```
pip install gitchecker
```

## Demo Usage
```python
import gitchecker
commit_info = \
    gitchecker.check_status_and_get_commit_info(repo_path="",
                                                warning_instead_of_error=False,
                                                ignore_untracked_files=False,
                                                ignore_files_regex=None,
                                                logger=None)

print("commit", commit_info)
```
The displayed values of the parameters are the default ones.

If a ```logger``` is provided, it will be used only if it has an ```error()``` 
or ```warning()``` method. The required method depends on the value of 
```warning_instead_of_error```. If no ```logger``` provided or no proper 
log function exists in ```logger``` , ```print()``` will be used instead.

Ignoring untracked files (```ignore_untracked_files=True```) or 
Ignoring by regex (```ignore_files_regex="regex"```) will ignore them completely,
not raising errors and not showing warnings.

## Testing
The GIT status must be clean to run functional test.

    python setup.py test

To run only unit tests, use:

    python -m pytest --pep8 --cov=gitchecker --cov-report=term-missing --cov-report=html -vv -x -k unit
