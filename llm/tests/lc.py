import unittest

prompt = """
The following is a system of a controller for a gate at a railway crossing - an intersection between a railway line and a road at the same level. 

Events: Approaching, Entering, Leaving, Lower, Raise

Requirements:

- When a train passes it requests to approach, enter, and then leave.
- The barriers are lowered when a train is approaching and then raised.
- A train may not enter while barriers are raised.
- The barriers may not be raised while a train is in the intersection zone, between its approaching and leaving.
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 4

    def req_1(self):
        mod_trace = [x for x in self.trace if x == "Approaching" or x == "Entering" or x == "Leaving"]
        should_be = ["Approaching", "Entering", "Leaving"]
        for i in range(len(mod_trace)):
            self.assertEqual(mod_trace[i], should_be[i % 3])

    def req_2(self):
        mod_trace = [x for x in self.trace if x == "Lower" or x == "Raise"]
        should_be = ["Lower", "Raise"]
        for i in range(len(mod_trace)):
            # if mod_trace[i] != should_be[i % 2]:
            #     print(self.trace)
            self.assertEqual(mod_trace[i], should_be[i % 2])
        should_lower = False
        already_lowered = False
        for i in range(len(self.trace)):
            if self.trace[i] == "Approaching":
                should_lower = not already_lowered
            if self.trace[i] == "Lower":
                if already_lowered or not should_lower:
                    print(self.trace)
                    assert False
                already_lowered = True
                should_lower = False
            if self.trace[i] == "Raise":
                already_lowered = False
                should_lower = False

    def req_3(self):
        raised = True
        for i in range(len(self.trace)):
            if self.trace[i] == "Entering":
                assert not raised
            if self.trace[i] == "Lower":
                raised = False
            if self.trace[i] == "Raise":
                raised = True

    def req_4(self):
        inside = False
        for i in range(len(self.trace)):
            if self.trace[i] == "Approaching":
                inside = True
            if self.trace[i] == "Leaving":
                inside = False
            if self.trace[i] == "Raise":
                assert not inside

