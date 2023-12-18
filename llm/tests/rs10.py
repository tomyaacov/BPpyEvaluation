import unittest

prompt = """

Event List:

Coin Insertion (Event A): A user inserts a coin into the vending machine.
Product Selection (Event B): The user selects a product they want to purchase.
Product Dispensation (Event C): The vending machine dispenses the selected product.
Change Return (Event D): The vending machine returns change to the user.
Refill (Event E): The vending machine is refilled with products.
Maintenance (Event F): Maintenance personnel perform maintenance on the vending machine.
Rejection (Event G): The vending machine rejects a Product Selection.

Requirements List:


Event B (Product Selection) can only occur if at least one coin has been inserted (Event A).
Event C (Product Dispensation) can only occur if a product has been selected (Event B) and two or more coins are inserted (Event A).
Event G (Rejection) can only occur if a product has been selected (Event B) and less than two coins are inserted (Event A).
If Event C (Product Dispensation) occurs, Event D (Change Return) should follow if more than two coins are inserted (Event A).
Event E (Refill) can only occur when the vending machine is not currently in use, i.e., not between events A and G/C.
Event F (Maintenance) can only happen after Event E (Refill).
Between any two occurrences of Event E (Refill), there should be no more than 2 occurrences of Event F (Maintenance).
Between the occurrence of Event E (Refill) and Event F (Maintenance), there should be no occurrences of Event A (Coin Insertion).
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 8

    def req_1(self):
        b_indices = [i for i, event in enumerate(self.trace) if event == 'B']
        for b_ind in b_indices:
            if 'A' not in self.trace[:b_ind]:
                self.fail("Event B should occur after at least one coin insertion (Event A)")

    def req_2(self):
        c_indices = [i for i, event in enumerate(self.trace) if event == 'C']
        for c_ind in c_indices:
            if 'B' not in self.trace[:c_ind] and self.trace[:c_ind].count('A') < 2:
                self.fail("Event C should occur after a product selection (Event B)")

    def req_3(self):
        g_indices = [i for i, event in enumerate(self.trace) if event == 'G']
        for g_ind in g_indices:
            if 'B' not in self.trace[:g_ind] and self.trace[:g_ind].count('A') >= 2:
                self.fail("Event G should occur after a product selection (Event B) and less than two coin insertions (Event A)")

    def req_4(self):
        c_indices = [i for i, event in enumerate(self.trace) if event == 'C']
        for c_ind in c_indices:
            if self.trace[:c_ind].count('A') > 2:
                assert 'D' == self.trace[c_ind+1]

    def req_5(self):
        e_allowed = True
        for event in self.trace:
            if event == 'A':
                e_allowed = False
            elif event == 'G' or event == 'C':
                e_allowed = True
            elif event == 'E' and not e_allowed:
                self.fail()

    def req_6(self):
        f_indices = [i for i, event in enumerate(self.trace) if event == 'F']
        for f_ind in f_indices:
            if 'E' not in self.trace[:f_ind]:
                self.fail("Event F should occur after a refill (Event E)")

    def req_7(self):
        e_indices = [i for i, event in enumerate(self.trace) if event == 'E']
        for i in range(len(e_indices) - 1):
            if self.trace[e_indices[i]:e_indices[i+1]].count('F') > 2:
                self.fail("Between any two occurrences of Event E (Refill), there should be no more than 2 occurrences of Event F (Maintenance)")

    def req_8(self):
        a_allowed = True
        for event in self.trace:
            if event == 'E':
                a_allowed = False
            elif event == 'F':
                a_allowed = True
            elif event == 'A' and not a_allowed:
                self.fail("Between the occurrence of Event E (Refill) and Event F (Maintenance), there should be no occurrences of Event A (Coin Insertion)")






