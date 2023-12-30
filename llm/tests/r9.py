import unittest

prompt = """
Events: A, B, C, D

Requirements:

- A should occur at least 5 times.
- B should always be followed by C.
- There must be at least one occurrence of D before any occurrence of B.
- The sequence A, B, C is forbidden.
- There should be no more than 2 consecutive occurrences of A.
- There should be at least one occurrence of B between any two occurrences of C.
- There should be no more than 1 occurrence of D between any two occurrences of A.
- After the third occurrence of A, there should be a sequence of at least two consecutive occurrences of D.
- The last event in the trace must be A.
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 9

    def req_1(self):
        self.assertGreaterEqual(self.trace.count('A'), 5)

    def req_2(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'B' and self.trace[i + 1] != 'C':
                self.fail("Requirement 2 failed")

    def req_3(self):
        d_found = False
        for event in self.trace:
            if event == 'D':
                d_found = True
            elif event == 'B' and not d_found:
                self.fail("Requirement 3 failed")

    def req_4(self):
        for i in range(len(self.trace) - 2):
            if self.trace[i:i + 3] == ['A', 'B', 'C']:
                self.fail("Requirement 4 failed")

    def req_5(self):
        consecutive_a_count = 0
        for event in self.trace:
            if event == 'A':
                consecutive_a_count += 1
                if consecutive_a_count > 2:
                    self.fail("Requirement 5 failed")
            else:
                consecutive_a_count = 0

    def req_6(self):
        t = [x for x in self.trace if x in ['B', 'C']]
        for i in range(len(t)-1):
            if t[i] == 'C' and t[i+1] == 'C':
                self.fail("Requirement 6 failed")

    def req_7(self):
        d_count = 0
        for event in self.trace:
            if event == 'D':
                d_count += 1
            elif event == 'A':
                if d_count > 1:
                    self.fail("Requirement 7 failed")
                d_count = 0

    def req_8(self):
        found_a = 0
        consecutive_d_count = 0
        for event in self.trace:
            if event == 'A':
                found_a += 1
            elif found_a == 3 and event == 'D':
                consecutive_d_count += 1
            elif found_a == 3 and event != 'D':
                if consecutive_d_count < 2:
                    self.fail("Requirement 8 failed")

    def req_9(self):
        self.assertEqual(self.trace[-1], 'A')




