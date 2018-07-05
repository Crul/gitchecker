[![Travis build](https://travis-ci.org/Crul/gitchecker.svg?branch=dev)](https://travis-ci.org/Crul/gitchecker) 
[![Coverage Status](https://coveralls.io/repos/github/Crul/gitchecker/badge.svg?branch=dev)](https://coveralls.io/github/Crul/gitchecker?branch=dev)
[![pypi-version](https://img.shields.io/pypi/v/gitchecker.svg)](https://pypi.org/project/gitchecker/)
[![pypi-wheel](https://img.shields.io/pypi/wheel/gitchecker.svg)](https://pypi.org/project/gitchecker/)
[![pypi-format](https://img.shields.io/pypi/format/gitchecker.svg)](https://pypi.org/project/gitchecker/)
[![pypi-pyversions](https://img.shields.io/pypi/pyversions/gitchecker.svg)](https://pypi.org/project/gitchecker/)
[![pypi-implementation](https://img.shields.io/pypi/implementation/gitchecker.svg)](https://pypi.org/project/gitchecker/)
[![pypi-status](https://img.shields.io/pypi/status/gitchecker.svg)](https://pypi.org/project/gitchecker/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/db52183d1abe4ae389fddbf9911c83b2?branch=dev)](https://www.codacy.com/app/Crul/gitchecker)
# Python GIT tool to check pending changes 

```gitchecker.check_clean_status()``` checks if there is any pending changes 
in GIT repository status and returns the last commit SHA (7 digits length). 
By default it raises an ```Exception``` if there are any pending changes but 
it can be configured to only show a warning instead.

## Install

```
pip install gitchecker
```

## Demo Usage
```python
import gitchecker
commit_sha = gitchecker.check_clean_status(repo_path="",
                                           warning_instead_of_error=False,
                                           ignore_untracked_files=False,
                                           ignore_files_regex=None,
                                           logger=None)
print("commit", commit_sha)
```
The displayed values of the parameters are the default ones.

If a ```logger``` is provided, it will be used only if it has an ```error()``` 
or ```warning()``` method. The required method depends on the value of 
```warning_instead_of_error```. If no ```logger``` provided or no proper 
log function exists in ```logger``` , ```print()``` will be used instead.

Ignoring untracked files (```ignore_untracked_files=True```) or 
Ignoring by regex (```ignore_files_regex```) will ignore them completely,
not raising errors and not showing warnings.

## Testing
Launch: ```python setup.py test```
The GIT status must be clean to run functional test.
