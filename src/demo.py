import gitchecker

commit_sha = gitchecker.check_clean_status(repo_path="..",
                                           warning_instead_of_error=False,
                                           ignore_untracked_files=False,
                                           ignore_files_regex=None,
                                           logger=None)

print("commit", commit_sha)
