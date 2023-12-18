import unittest

prompt = """
Events: A, B, C, D, E, F, G, H, I, J

Requirements:

- A should occur at least 7 times.
- B should always be followed by C within the next 2 events.
- There should be no consecutive G events.
- H should occur at least 4 times.
- The last event in the trace must be J.
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 5

    def req_1(self):
        self.assertGreaterEqual(self.trace.count('A'), 7)

    def req_2(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'B':
                found_c = False
                for j in range(i + 1, min(i + 3, len(self.trace))):
                    if self.trace[j] == 'C':
                        found_c = True
                        break
                if not found_c:
                    self.fail("Requirement 2 failed")

    def req_3(self):
        consecutive_g_count = 0
        for event in self.trace:
            if event == 'G':
                consecutive_g_count += 1
                if consecutive_g_count > 1:
                    self.fail("Requirement 3 failed")
            else:
                consecutive_g_count = 0

    def req_4(self):
        self.assertGreaterEqual(self.trace.count('H'), 4)

    def req_5(self):
        self.assertEqual(self.trace[-1], 'J')




