import unittest

prompt = """
Events in Online Shopping Cart System:

- User Adding Item to Cart (Event A): A user adds an item to their shopping cart.
- User Removing Item from Cart (Event B): A user removes an item from their shopping cart.
- User Proceeding to Checkout (Event C): A user proceeds to the checkout process.

Requirements for Online Shopping Cart System:

Event A Adding Items:

- Event A (User Adding Item to Cart) should occur when a user adds items to their cart.

Event B Removing Items:

- Event B (User Removing Item from Cart) should occur when a user removes items from their cart.

Event C Checkout Process:

- Event C (User Proceeding to Checkout) should follow Event A (User Adding Item to Cart) and indicate that the user wants to proceed with the checkout process.

Cart Must Not Be Empty at Checkout:

- Event C (User Proceeding to Checkout) should only occur if the user's shopping cart is not empty. 
The total number of items in the cart (sum of quantities of individual items) should always be consistent with the user's cart view. 
Event A (Adding Items) and Event B (Removing Items) should maintain this consistency.
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 4

    def req_1(self):
        self.assertIn('A', self.trace)

    def req_2(self):
        self.assertIn('B', self.trace)

    def req_3(self):
        f = 0
        for i in range(len(self.trace)):
            if "C" == self.trace[i]:
                self.assertTrue('A' in self.trace[f:i])
                f = i

    def req_4(self):
        cart_items = 0
        for event in self.trace:
            if event == 'A':
                cart_items += 1
            elif event == 'B':
                cart_items -= 1
            elif event == 'C':
                self.assertTrue(cart_items > 0)
                cart_items = 0

