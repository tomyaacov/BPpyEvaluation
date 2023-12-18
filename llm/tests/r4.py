import unittest

prompt = """
Events: A, B, C, D, E, F, G, H, I

Requirements:

- A should occur at least 6 times.
- B should always be followed by C.
- If D occurs, it should be followed by E within the next 2 events.
- There should be no consecutive F events.
- G should occur at least 4 times.
- H should occur exactly 3 times.
- After the second occurrence of H, there should be a sequence of at least three consecutive I events.
- There should be no more than 3 occurrences of G between any two A events.
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 8

    def req_1(self):
        self.assertGreaterEqual(self.trace.count('A'), 6)

    def req_2(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'B' and self.trace[i + 1] != 'C':
                self.fail("Requirement 2 failed")

    def req_3(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'D':
                found_e = False
                for j in range(i + 1, min(i + 3, len(self.trace))):
                    if self.trace[j] == 'E':
                        found_e = True
                        break
                if not found_e:
                    self.fail("Requirement 3 failed")

    def req_4(self):
        consecutive_f_count = 0
        for event in self.trace:
            if event == 'F':
                consecutive_f_count += 1
                if consecutive_f_count > 1:
                    self.fail("Requirement 4 failed")
            else:
                consecutive_f_count = 0

    def req_5(self):
        self.assertGreaterEqual(self.trace.count('G'), 4)

    def req_6(self):
        self.assertEqual(self.trace.count('H'), 3)

    def req_7(self):
        number_of_h = 0
        consecutive_i_count = 0
        for event in self.trace:
            if event == 'H':
                number_of_h += 1
            elif number_of_h == 2 and event == 'I':
                consecutive_i_count += 1
            elif number_of_h == 2 and event != 'I':
                assert consecutive_i_count >= 3

    def req_8(self):
        a_count = 0
        g_count = 0
        for event in self.trace:
            if event == 'A':
                a_count += 1
            elif event == 'G':
                g_count += 1
                if g_count > 3:
                    self.fail("Requirement 8 failed")
            if a_count % 2 == 0:
                g_count = 0


