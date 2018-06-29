from tests.functional_config.common import ExpectedResults, FuncTestConfig, test_configs


test_id = "staged file"


def setup(self, stage=True):
    foo_filename = self._create_foo_file()
    self._stage(foo_filename)
    self._commit("auto-commit: {} test".format(test_id))
    self._modify_file(foo_filename)
    if stage:
        self._stage(foo_filename)

    return foo_filename


def teardown(self, foo_filename):
    self.repo.head.reset("HEAD~1")
    self._remove_file(foo_filename)

expected_results = ExpectedResults(staged_files=1)
test_configs.append(FuncTestConfig(test_id, setup, teardown, expected_results))
