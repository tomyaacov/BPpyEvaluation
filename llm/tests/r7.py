import unittest

prompt = """
Events: A, B, C, D, E, F, G, H, I, J

Requirements:

- A should occur at least 5 times.
- B should always be followed by C within the next 3 events.
- There must be at least one occurrence of D before any occurrence of E.
- The sequence F, G, H is allowed at most twice.
- I should occur exactly 4 times.
- J should never occur immediately after I.
- After the third occurrence of I, there should be a sequence of at least two consecutive J events.
- There should be no more than 2 occurrences of G between any two A events.
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 8

    def req_1(self):
        self.assertGreaterEqual(self.trace.count('A'), 5)

    def req_2(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'B':
                found_c = False
                for j in range(i + 1, min(i + 4, len(self.trace))):
                    if self.trace[j] == 'C':
                        found_c = True
                        break
                if not found_c:
                    self.fail("Requirement 2 failed")

    def req_3(self):
        d_found = False
        for event in self.trace:
            if event == 'D':
                d_found = True
            elif event == 'E' and not d_found:
                self.fail("Requirement 3 failed")

    def req_4(self):
        fgh_count = 0
        for i in range(len(self.trace) - 2):
            if self.trace[i:i+3] == ['F', 'G', 'H']:
                fgh_count += 1
                if fgh_count > 2:
                    self.fail("Requirement 4 failed")

    def req_5(self):
        self.assertEqual(self.trace.count('I'), 4)

    def req_6(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'I' and self.trace[i + 1] == 'J':
                self.fail("Requirement 6 failed")

    def req_7(self):
        found_i = 0
        consecutive_j_count = 0
        for event in self.trace:
            if event == 'I':
                found_i += 1
            elif found_i == 3 and event == 'J':
                consecutive_j_count += 1
            elif found_i == 3 and event != 'J':
                if consecutive_j_count < 2:
                    self.fail("Requirement 7 failed")

    def req_8(self):
        a_count = 0
        g_count = 0
        for event in self.trace:
            if event == 'A':
                a_count += 1
            elif event == 'G':
                g_count += 1
                if g_count > 2:
                    self.fail("Requirement 8 failed")
            if a_count == 2:
                g_count = 0




