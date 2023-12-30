import unittest

prompt = """
Events: A, B, C, D, E

Requirements:

- A should happen at least 3 times.
- If C occurs right after A, then B must happen immediately.
- There should be no consecutive As.
- B should occur at least once.
- D and E should always occur together.
- A and C should not occur consecutively more than twice in a row.
- There should be no more than 2 consecutive occurrences of B.
- A, B, C, D, and E should occur at least once each in any sequence.
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 8

    def req_1(self):
        self.assertGreaterEqual(self.trace.count('A'), 3)

    def req_2(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'A' and self.trace[i + 1] == 'C':
                if i == len(self.trace) - 2:
                    assert False
                self.assertEqual(self.trace[i + 2], 'B')

    def req_3(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'A':
                self.assertNotEqual(self.trace[i + 1], 'A')

    def req_4(self):
        self.assertIn('B', self.trace)

    def req_5(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'D':
                self.assertEqual(self.trace[i + 1], 'E')

    def req_6(self):
        consecutive_count = 0
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'A' and self.trace[i + 1] == 'C':
                consecutive_count += 1
            else:
                consecutive_count = 0
            self.assertLessEqual(consecutive_count, 2)

    def req_7(self):
        consecutive_b_count = 0
        for event in self.trace:
            if event == 'B':
                consecutive_b_count += 1
            else:
                consecutive_b_count = 0
            self.assertLessEqual(consecutive_b_count, 2)

    def req_8(self):
        self.assertIn('A', self.trace)
        self.assertIn('B', self.trace)
        self.assertIn('C', self.trace)
        self.assertIn('D', self.trace)
        self.assertIn('E', self.trace)

