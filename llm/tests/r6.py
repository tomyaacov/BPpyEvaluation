import unittest

prompt = """
Events: X, Y, Z, A, B, C, D, E, F, G, H

Requirements:

- X should occur at least 5 times.
- Y should never occur consecutively more than twice.
- There must be at least one A between two B events.
- The sequence D, E, F is forbidden.
- G should occur exactly 3 times.
- H should occur at most 2 times.
- After the second occurrence of H, there should be a sequence of at least two consecutive G events.
- There should be no more than 3 occurrences of Y between any two X events.
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 8

    def req_1(self):
        self.assertGreaterEqual(self.trace.count('X'), 5)

    def req_2(self):
        consecutive_y_count = 0
        for event in self.trace:
            if event == 'Y':
                consecutive_y_count += 1
                if consecutive_y_count > 2:
                    self.fail("Requirement 2 failed")
            else:
                consecutive_y_count = 0

    def req_3(self):
        t = [x for x in self.trace if x in ['A', 'B']]
        for i in range(len(t)-1):
            if t[i] == 'B' and t[i+1] == 'B':
                self.fail("Requirement 3 failed")

    def req_4(self):
        for i in range(len(self.trace) - 2):
            if self.trace[i:i + 3] == ['D', 'E', 'F']:
                self.fail("Requirement 4 failed")

    def req_5(self):
        self.assertEqual(self.trace.count('G'), 3)

    def req_6(self):
        self.assertLessEqual(self.trace.count('H'), 2)

    def req_7(self):
        found_first_h = False
        found_second_h = False
        found_g = False
        consecutive_g_count = 0
        for event in self.trace:
            if (not found_first_h) and event == 'H':
                found_first_h = True
            elif found_first_h and event == 'H':
                found_second_h = True
            elif found_second_h and (not found_g) and event == 'G':
                found_g = True
                consecutive_g_count = 1
            elif found_second_h and found_g and event == 'G':
                consecutive_g_count += 1
            elif found_second_h and found_g and event != 'G':
                if consecutive_g_count < 2:
                    self.fail("Requirement 7 failed")

    def req_8(self):
        x_count = 0
        y_count = 0
        for event in self.trace:
            if event == 'X':
                x_count += 1
            elif event == 'Y':
                y_count += 1
                if y_count > 3:
                    self.fail("Requirement 8 failed")
            if x_count == 2:
                y_count = 0




