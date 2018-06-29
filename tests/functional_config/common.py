from collections import namedtuple

ExpectedResults = \
    namedtuple("ExpectedResults", ["staged_files", "unstaged_files", "untracked_files"])

ExpectedResults.__new__.__defaults__ = (0, 0, 0)

FuncTestConfig = namedtuple("TestConfig", ["id", "setup", "teardown", "expected_results"])

test_configs = []
