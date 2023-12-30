import unittest

prompt = """
Events: A, B, C, D

Requirements:

- A should occur at least 2 times.
- A should never occur immediately after D.
- The sequence B, C, D is forbidden.
- There should be at least one occurrence of A between any two occurrences of B.
- D should not occur after C until A occurs at least once.
- There should be no consecutive occurrences of D.
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 6

    def req_1(self):
        self.assertGreaterEqual(self.trace.count('A'), 2)

    def req_2(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'D' and self.trace[i + 1] == 'A':
                self.fail("Requirement 1 failed")

    def req_3(self):
        for i in range(len(self.trace) - 2):
            if self.trace[i:i + 3] == ['B', 'C', 'D']:
                self.fail("Requirement 2 failed")

    def req_4(self):
        a_count = 0
        for event in self.trace:
            if event == 'A':
                a_count += 1
            elif event == 'B':
                if a_count < 1:
                    self.fail("Requirement 3 failed")
                a_count = 0

    def req_5(self):
        d_allowed = True
        for event in self.trace:
            if event == 'D':
                if not d_allowed:
                    self.fail("Requirement 4 failed")
            elif event == 'C':
                d_allowed = False
            elif event == 'A':
                d_allowed = True

    def req_6(self):
        consecutive_d_count = 0
        for event in self.trace:
            if event == 'D':
                consecutive_d_count += 1
                if consecutive_d_count > 1:
                    self.fail("Requirement 5 failed")
            else:
                consecutive_d_count = 0




