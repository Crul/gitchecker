[![Travis build](https://travis-ci.org/Crul/gitchecker.svg?branch=dev)](https://travis-ci.org/Crul/gitchecker) 
[![Coverage Status](https://coveralls.io/repos/github/Crul/gitchecker/badge.svg?branch=dev)](https://coveralls.io/github/Crul/gitchecker?branch=dev)
# Python GIT tool to check pending changes 

```gitchecker.check_clean_status()``` checks if there is any pending changes 
in GIT repository status and returns the last commit SHA (7 digits length). 
By default it raises an ```Exception``` if there are any pending changes but 
it can be configured to only show a warning instead.

## Demo Usage
```python
import gitchecker
commit_sha = gitchecker.check_clean_status(repo_path="",
                                           warning_instead_of_error=False,
                                           ignore_untracked_files=False,
                                           logger=None)
print("commit", commit_sha)
```
The displayed values of the parameters are the default ones.

If a ```logger``` is provided, it will be used only if it has an ```error()``` 
or ```warning()``` method. The required method depends on the value of 
```warning_instead_of_error```. If no ```logger``` provided or no proper 
log function exists in ```logger``` , ```print()``` will be used instead.

Ignoring untracked files (```ignore_untracked_files=True```) will ignore them completely, 
not raising errors and not showing warnings.

## Testing
Launch: ```python setup.py test```
The GIT status must be clean to run functional test.
