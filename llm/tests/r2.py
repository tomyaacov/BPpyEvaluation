import unittest

prompt = """
Events: D, E, F

Requirements:

- D should occur at least 4 times.
- E should follow D within the next 2 events.
- If F occurs, it should always be followed by E.
- There should be no consecutive D events.
- E should occur at least 5 times.
- F should occur at most 2 times.
- E should not occur after F.
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 7

    def req_1(self):
        self.assertGreaterEqual(self.trace.count('D'), 4)

    def req_2(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'D':
                ok = False
                for j in range(i + 1, min(i + 3, len(self.trace))):
                    if self.trace[j] == 'E':
                        ok = True
                        break
                assert ok

    def req_3(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'F' and self.trace[i + 1] != 'E':
                self.fail("Requirement 3 failed")

    def req_4(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'D' and self.trace[i + 1] == 'D':
                self.fail("Requirement 4 failed")

    def req_5(self):
        self.assertGreaterEqual(self.trace.count('E'), 5)

    def req_6(self):
        self.assertLessEqual(self.trace.count('F'), 2)

    def req_7(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'F' and 'E' in self.trace[i + 1:]:
                self.fail("Requirement 7 failed")

