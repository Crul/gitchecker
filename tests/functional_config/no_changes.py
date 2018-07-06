from tests.functional_config.common import ExpectedResults, FuncTestConfig, test_configs


test_id = "no changes"


def setup(self):
    pass


def teardown(self, foo_filename):
    pass


expected_results = ExpectedResults()
test_configs.append(FuncTestConfig(test_id, setup, teardown, expected_results))
