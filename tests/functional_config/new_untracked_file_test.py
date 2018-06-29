from tests.functional_config.common import ExpectedResults, FuncTestConfig, test_configs


test_id = "new untracked file"


def setup(self):
    foo_filename = self._create_foo_file()

    return foo_filename


def teardown(self, foo_filename):
    self._remove_file(foo_filename)


expected_results = ExpectedResults(untracked_files=1)
test_configs.append(FuncTestConfig(test_id, setup, teardown, expected_results))
