import unittest

prompt = """
Event List:

- Car Reservation (Event A): A customer makes a reservation for a rental car.
- Car Pickup (Event B): The customer picks up the reserved rental car.
- Car Return (Event C): The customer returns the rental car after use.
- Payment (Event D): The customer pays for the rental service.
- Late Return Penalty (Event E): If a customer returns the car late, a penalty is applied.
- Car Maintenance (Event F): Rental cars undergo routine maintenance.
- Customer Registration (Event G): A new customer registers with the rental system.
- Car Availability (Event H): A rental car becomes available for reservation.
- Customer Feedback (Event I): Customers provide feedback on their rental experience.

Requirements List:

- Event A (Car Reservation) should occur before Event B (Car Pickup).
- Event B (Car Pickup) should be followed by Event C (Car Return).
- Event D (Payment) should occur after Event C (Car Return).
- If Event E (Late Return Penalty) occurs, it should follow Event C (Car Return).
- Event F (Car Maintenance) should not occur while a car is reserved or rented (between Events A and C).
- Event G (Customer Registration) should occur before any reservation (Event A) by the same customer.
- There should be no more than one occurrence of Event G (Customer Registration) between any two occurrences of Event A (Car Reservation) by the same customer.
- There should be no more than 2 occurrences of Event H (Car Availability) between any two occurrences of Event A (Car Reservation).
- Event I (Customer Feedback) should occur after Event C (Car Return) for each rental.
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 9

    def req_1(self):
        self.assertTrue('A' in self.trace and 'B' in self.trace)
        a_index = self.trace.index('A')
        b_index = self.trace.index('B')
        self.assertTrue(a_index < b_index)

    def req_2(self):
        self.assertTrue('B' in self.trace and 'C' in self.trace)
        b_index = self.trace.index('B')
        c_index = self.trace.index('C')
        self.assertTrue(b_index < c_index)

    def req_3(self):
        self.assertTrue('C' in self.trace and 'D' in self.trace)
        c_index = self.trace.index('C')
        d_index = self.trace.index('D')
        self.assertTrue(c_index < d_index)

    def req_4(self):
        if 'E' in self.trace:
            e_index = self.trace.index('E')
            c_index = self.trace.index('C')
            self.assertTrue(e_index > c_index)

    def req_5(self):
        for i in range(len(self.trace)):
            if self.trace[i] == 'F':
                self.assertFalse('A' in self.trace[i+1:] and 'C' in self.trace[i+1:])

    def req_6(self):
        a_indices = [i for i, event in enumerate(self.trace) if event == 'A']
        g_indices = [i for i, event in enumerate(self.trace) if event == 'G']
        for g_indices, a_index in zip(g_indices, a_indices):
            self.assertTrue(g_indices < a_index)

    def req_7(self):
        a_indices = [i for i, event in enumerate(self.trace) if event == 'A']
        for i in range(len(a_indices) - 1):
            g_count_between = self.trace[a_indices[i]:a_indices[i+1]].count('G')
            self.assertTrue(g_count_between <= 1)

    def req_8(self):
        a_indices = [i for i, event in enumerate(self.trace) if event == 'A']
        for i in range(len(a_indices) - 1):
            h_count_between = self.trace[a_indices[i]:a_indices[i+1]].count('H')
            self.assertTrue(h_count_between <= 2)

    def req_9(self):
        c_indices = [i for i, event in enumerate(self.trace) if event == 'C']
        for c_index in c_indices:
            self.assertTrue('I' in self.trace[c_index+1:])






