import gitchecker

commit_info = \
    gitchecker.check_status_and_get_commit_info(repo_path="..",
                                                warning_instead_of_error=True,
                                                ignore_untracked_files=False,
                                                ignore_files_regex=None,
                                                logger=None)

print("commit info:", commit_info)
