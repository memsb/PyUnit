class TestSuite:

    def __init__(self):
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def run(self, result):
        for test in self.tests:
            test.run(result)


class TestCase:
    def __init__(self, name):
        self.name = name
        self.log = ""

    def set_up(self):
        pass

    def tear_down(self):
        pass

    def run(self, result):
        result.test_started()
        self.set_up()
        try:
            method = getattr(self, self.name)
            method()
        except Exception:
            result.test_failed()
        self.tear_down()


class TestResult:
    def __init__(self):
        self.run_count = 0
        self.failed_count = 0

    def test_started(self):
        self.run_count = self.run_count + 1

    def test_failed(self):
        self.failed_count = self.failed_count + 1

    def summary(self):
        return f"{self.run_count} run, {self.failed_count} failed"


class WasRun(TestCase):
    def __init__(self, name):
        TestCase.__init__(self, name)

    def set_up(self):
        self.log = self.log + "set_up "

    def tear_down(self):
        self.log = self.log + "tear_down "

    def test_method(self):
        self.log = self.log + "test_method "

    def test_broken_method(self):
        raise Exception


class TestCaseTest(TestCase):

    def set_up(self):
        self.result = TestResult()

    def test_template_method(self):
        test = WasRun("test_method")
        test.run(self.result)
        assert test.log == "set_up test_method tear_down "

    def test_result(self):
        test = WasRun("test_method")
        test.run(self.result)
        assert self.result.summary() == "1 run, 0 failed"

    def test_failed_result(self):
        test = WasRun("test_broken_method")
        test.run(self.result)
        assert self.result.summary() == "1 run, 1 failed"

    def test_failed_result_formatting(self):
        self.result.test_started()
        self.result.test_failed()
        assert self.result.summary() == "1 run, 1 failed"

    def test_suite(self):
        suite = TestSuite()
        suite.add(WasRun("test_method"))
        suite.add(WasRun("test_broken_method"))
        suite.run(self.result)

        assert self.result.summary() == "2 run, 1 failed"


test_suite = TestSuite()
test_suite.add(TestCaseTest("test_template_method"))
test_suite.add(TestCaseTest("test_result"))
test_suite.add(TestCaseTest("test_failed_result"))
test_suite.add(TestCaseTest("test_suite"))
results = TestResult()
test_suite.run(results)
print(results.summary())
