import unittest

prompt = """
Event List:

- Customer Arrives (Event A): A customer arrives at the restaurant.
- Customer Places an Order (Event B): The customer places an order for food.
- Kitchen Receives Order (Event C): The kitchen receives the customer's order.
- Food Preparation (Event D): The kitchen starts preparing the food.
- Food Ready (Event E): The kitchen notifies that the food is ready.
- Customer Receives Food (Event F): The customer receives the prepared food.
- Customer Pays Bill (Event G): The customer pays their bill.
- Table Clearing (Event H): The restaurant staff clears the table after the customer leaves.
- Customer Leaves (Event I): The customer leaves the restaurant.

Requirements List:

- Event A (Customer Arrives) should occur when a customer enters the restaurant.
- Event B (Customer Places an Order) should follow Event A (Customer Arrives).
- Event C (Kitchen Receives Order) should follow Event B (Customer Places an Order).
- Event F (Customer Receives Food) should occur after Event E (Food Ready).
- Event G (Customer Pays Bill) should follow Event F (Customer Receives Food).
- Event H (Table Clearing) should occur after Event G (Customer Pays Bill).
- If Event C (Kitchen Receives Order) occurs, it must be followed by Event D (Food Preparation) within the next 3 events.
- If Event G (Customer Pays Bill) occurs, it should be followed by Event I (Customer Leaves) within the next 2 events.
- Event E (Food Ready) should not occur more than once between Event C (Kitchen Receives Order) and Event G (Customer Pays Bill).
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 9

    def req_1(self):
        self.assertTrue("A" in self.trace)

    def req_2(self):
        if "A" not in self.trace or "B" not in self.trace:
            self.fail("Event A or Event B missing")
        a_ind = self.trace.index('A')
        b_ind = self.trace.index('B')
        self.assertTrue(a_ind < b_ind)

    def req_3(self):
        if "B" not in self.trace or "C" not in self.trace:
            self.fail("Event B or Event C missing")
        b_ind = self.trace.index('B')
        c_ind = self.trace.index('C')
        self.assertTrue(b_ind < c_ind)

    def req_4(self):
        if "E" not in self.trace or "F" not in self.trace:
            self.fail("Event E or Event F missing")
        e_ind = self.trace.index('E')
        f_ind = self.trace.index('F')
        self.assertTrue(e_ind < f_ind)

    def req_5(self):
        if "F" not in self.trace or "G" not in self.trace:
            self.fail("Event F or Event G missing")
        f_ind = self.trace.index('F')
        g_ind = self.trace.index('G')
        self.assertTrue(f_ind < g_ind)

    def req_6(self):
        if "G" not in self.trace or "H" not in self.trace:
            self.fail("Event G or Event H missing")
        g_ind = self.trace.index('G')
        h_ind = self.trace.index('H')
        self.assertTrue(g_ind < h_ind)

    def req_7(self):
        c_indices = [i for i, event in enumerate(self.trace) if event == 'C']
        for c_ind in c_indices:
            if "D" not in self.trace[c_ind+1:c_ind+4]:
                self.fail("Event D should follow Event C within the next 3 events")

    def req_8(self):
        g_indices = [i for i, event in enumerate(self.trace) if event == 'G']
        for g_ind in g_indices:
            if "I" not in self.trace[g_ind+1:g_ind+3]:
                self.fail("Event I should follow Event G within the next 2 events")

    def req_9(self):
        c_indices = [i for i, event in enumerate(self.trace) if event == 'C']
        g_indices = [i for i, event in enumerate(self.trace) if event == 'G']
        if len(c_indices) > 0 and len(g_indices) > 0:
            for c_ind in c_indices:
                c_to_g_trace = self.trace[c_ind:g_indices[-1]+1]
                e_count = c_to_g_trace.count('E')
                self.assertTrue(e_count <= 1)






