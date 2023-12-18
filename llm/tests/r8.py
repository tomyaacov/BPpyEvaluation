import unittest

prompt = """
Events: A, B, C, D, E, F, G, H, I, J

Requirements:

- A should always be followed by either B, C, or D.
- E should never be followed by F.
- G and H should not occur consecutively.
- J should occur at least 3 times.
- After the first occurrence of J, there should be a sequence of at least two consecutive I events.
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 5

    def req_1(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'A' and self.trace[i + 1] not in ['B', 'C', 'D']:
                self.fail("Requirement 1 failed")

    def req_2(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'E' and self.trace[i + 1] == 'F':
                self.fail("Requirement 2 failed")

    def req_3(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] in ['G', 'H'] and self.trace[i + 1] in ['G', 'H']:
                self.fail("Requirement 3 failed")

    def req_4(self):
        self.assertGreaterEqual(self.trace.count('J'), 3)

    def req_5(self):
        found_first_j = False
        consecutive_i_count = 0
        for event in self.trace:
            if event == 'J':
                found_first_j = True
            elif found_first_j and event == 'I':
                consecutive_i_count += 1
            elif found_first_j and event != 'I':
                if consecutive_i_count < 2:
                    self.fail("Requirement 5 failed")




