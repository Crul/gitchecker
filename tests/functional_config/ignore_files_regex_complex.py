from time import time

from tests.functional_config.common import ExpectedResults, FuncTestConfig, test_configs


test_id = "ignore files regex - complex"
FOO_FILENAME = "{}.txt".format(str(time() * 1000))


def setup(self):
    self._create_foo_file(FOO_FILENAME)
    foo_filename = self._create_foo_file()

    return foo_filename


def teardown(self, foo_filename):
    self._remove_file(FOO_FILENAME)
    self._remove_file(foo_filename)


expected_results = ExpectedResults(untracked_files=1)
test_configs.append(FuncTestConfig(test_id,
                                   setup,
                                   teardown,
                                   expected_results,
                                   ignore_files_regex="^{}$".format(FOO_FILENAME)))
