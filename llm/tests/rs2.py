import unittest

prompt = """
Events in Vending Machine System:

- User Inserting Money (Event A): A user inserts coins or bills into the vending machine.
- User Selecting a Product (Event B): A user selects a product they want to purchase.
- Product Dispensing (Event C): The vending machine dispenses the selected product.

Requirements for Vending Machine System:

Event A Occurrence:

- Event A (User Inserting Money) should occur when a user inserts valid currency into the machine.

Event B Occurrence After A:

- Event B (User Selecting a Product) should only occur after Event A (User Inserting Money) to ensure that the user has sufficient funds to make a purchase.

Event C Following A and B:

- If Event C (Product Dispensing) occurs, it must follow both Event A and Event B.

No Consecutive As:

- There should be no consecutive occurrences of Event A (User Inserting Money) without an intervening Event B (User Selecting a Product).
"""

class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 4

    def req_1(self):
        assert "A" in self.trace

    def req_2(self):
        if "A" not in self.trace or "B" not in self.trace:  # is this the right approach?
            assert False
        a_ind = self.trace.index('A')
        b_ind = self.trace.index('B')
        assert a_ind < b_ind

    def req_3(self):
        if "A" not in self.trace or "B" not in self.trace or "C" not in self.trace:  # is this the right approach?
            assert False
        a_ind = self.trace.index('A')
        b_ind = self.trace.index('B')
        c_ind = self.trace.index('C')
        assert a_ind < c_ind and b_ind < c_ind

    def req_4(self):
        a_ok = True
        for e in self.trace:
            if e == 'A':
                if not a_ok:
                    assert False
                a_ok = False
            elif e == 'B':
                a_ok = True
        assert True

