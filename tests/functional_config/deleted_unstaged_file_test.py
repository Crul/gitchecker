from tests.functional_config.common import ExpectedResults, FuncTestConfig, test_configs
from tests.functional_config import deleted_staged_file_test


test_id = "deleted unstaged file"


def setup(self):
    return deleted_staged_file_test.setup(self, stage=False)


teardown = deleted_staged_file_test.teardown

expected_results = ExpectedResults(unstaged_files=1)
test_configs.append(FuncTestConfig(test_id, setup, teardown, expected_results))
