import unittest

prompt = """
Event List:

- Product Search (Event A): A customer searches for a product.
- Add to Cart (Event B): The customer adds a product to their shopping cart.
- Remove from Cart (Event C): The customer removes a product from their shopping cart.
- Checkout (Event D): The customer proceeds to checkout and makes a purchase.
- Payment (Event E): The customer completes the payment for the purchase.
- Order Confirmation (Event F): The customer receives an order confirmation.
- Shipping (Event G): The purchased items are prepared for shipping.
- Delivery (Event H): The purchased items are delivered to the customer.
- Return Request (Event I): The customer requests to return a product.

Requirements List:

- Event A (Product Search) must occur at least once before any checkout (Event D).
- Event B (Add to Cart) can occur multiple times, but it must follow at least one Event A (Product Search).
- Event C (Remove from Cart) can occur multiple times, but it must follow at least one Event B (Add to Cart).
- Event D (Checkout) can only occur if at least one Event B (Add to Cart) has occurred.
- After Event D (Checkout), there should be a sequence of at least two consecutive Events E (Payment).
- Events G (Shipping) and H (Delivery) should not occur consecutively.
- The last event in the trace must be Event H (Delivery) or Event I (Return Request).
- Event B (Add to Cart) should always be followed by Event C (Remove from Cart) within the next 2 events.
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 8

    def req_1(self):
        d_indices = [i for i, event in enumerate(self.trace) if event == 'D']
        for d_ind in d_indices:
            if 'A' not in self.trace[:d_ind]:
                self.fail("Event A should occur before Event D")

    def req_2(self):
        b_indices = [i for i, event in enumerate(self.trace) if event == 'B']
        for b_ind in b_indices:
            if 'A' not in self.trace[:b_ind]:
                self.fail("Event B should occur after Event A")

    def req_3(self):
        c_indices = [i for i, event in enumerate(self.trace) if event == 'C']
        for c_ind in c_indices:
            if 'B' not in self.trace[:c_ind]:
                self.fail("Event C should occur after Event B")

    def req_4(self):
        d_indices = [i for i, event in enumerate(self.trace) if event == 'D']
        for d_ind in d_indices:
            if 'B' not in self.trace[:d_ind]:
                self.fail("Event B should occur before Event D")

    def req_5(self):
        checkout_indices = [i for i, event in enumerate(self.trace) if event == 'D']
        for checkout_index in checkout_indices:
            consecutive_payment_count = 0
            for i in range(checkout_index + 1, len(self.trace)):
                if self.trace[i] == 'E':
                    consecutive_payment_count += 1
                else:
                    break
            self.assertTrue(consecutive_payment_count >= 2)

    def req_6(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'G' and self.trace[i + 1] == 'H':
                self.fail("Events G (Shipping) and H (Delivery) should not occur consecutively.")

    def req_7(self):
        assert self.trace[-1] == 'H' or self.trace[-1] == 'I'

    def req_8(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'B':
                next_events = self.trace[i + 1:i + 3]  # Check the next 2 events
                self.assertTrue('C' in next_events )






