import unittest

prompt = """
Events: X, Y, Z

Requirements:

- X should occur at least 5 times.
- Y should never occur consecutively more than twice.
- If Z occurs, it should be followed by X within the next 3 events.
- There should be no more than 2 occurrences of X between any two Y events.
- Y should occur at least 3 times.
- Z should occur exactly 2 times.
- After the first occurrence of Z, there should be a sequence of at least two consecutive Y events.
- The last event in the trace must be X.
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
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'Z':
                found_x = False
                for j in range(i + 1, min(i + 4, len(self.trace))):
                    if self.trace[j] == 'X':
                        found_x = True
                        break
                if not found_x:
                    self.fail("Requirement 3 failed")

    def req_4(self):
        x_count_between_y = 0
        for event in self.trace:
            if event == 'X':
                x_count_between_y += 1
            elif event == 'Y':
                if x_count_between_y > 2:
                    self.fail("Requirement 4 failed")
                x_count_between_y = 0

    def req_5(self):
        self.assertGreaterEqual(self.trace.count('Y'), 3)

    def req_6(self):
        self.assertEqual(self.trace.count('Z'), 2)

    def req_7(self):
        found_first_z = False
        consecutive_y_count = 0
        for event in self.trace:
            if event == 'Z':
                found_first_z = True
                consecutive_y_count = 0
            elif found_first_z and event == 'Y':
                consecutive_y_count += 1
            elif found_first_z and event != 'Y':
                if consecutive_y_count < 2:
                    self.fail("Requirement 7 failed")

    def req_8(self):
        print(self.trace)
        self.assertEqual(self.trace[-1], 'X')

