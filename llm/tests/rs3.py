import unittest

prompt = """
Event List:

- User Checking Out a Book (Event A): A user checks out a book from the library.
- User Returning a Book (Event B): A user returns a previously borrowed book to the library.
- Book Available for Checkout (Event C): A book becomes available for checkout by other users.
- Late Book Return (Event D): A user returns a book after the due date.
- Book Reservations (Event E): Users can reserve books that are currently checked out.
- Late Book Return Notice (Event F): The system generates a late book return notice for users who return books late.
- Book Request (Event G): Users can request specific books to be made available.
- User Fine (Event H): The system records fines imposed on users for overdue books.
- Book Request Fulfillment (Event I): The library fulfills a user's book request.
- User Account Update (Event Y): User account information is updated.

Requirements List:

- Event A (User Checking Out a Book) should occur when a user selects a book for checkout.
- Event B (User Returning a Book) should occur after Event A (User Checking Out a Book).
- If Event C (Book Available for Checkout) occurs, it must follow Event B (User Returning a Book).
- The sequence of events D (Late Book Return), E (Book Reservations), and F (Late Book Return Notice) is forbidden. If D occurs, it should not be followed by E and then F in succession.
- If Event D (Late Book Return) occurs, it should be followed by Event E (Book Reservations) within the next 2 events.
- After the second occurrence of Event H (User Fine), there should be a sequence of at least three consecutive Event I (Book Request Fulfillment) events.
- There should be no more than 3 occurrences of Event G (Book Request) between any two occurrences of Event A (User Checking Out a Book).
- Event Y (User Account Update) should never occur consecutively more than twice.
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 8

    def req_1(self):
        assert "A" in self.trace

    def req_2(self):
        if "A" not in self.trace or "B" not in self.trace:
            assert False
        a_ind = self.trace.index('A')
        b_ind = self.trace.index('B')
        assert a_ind < b_ind

    def req_3(self):
        if "B" not in self.trace or "C" not in self.trace:
            assert False
        b_ind = self.trace.index('B')
        c_ind = self.trace.index('C')
        assert b_ind < c_ind

    def req_4(self):
        for i in range(len(self.trace) - 2):
            if self.trace[i:i+3] == ['D', 'E', 'F']:
                assert False
        assert True

    def req_5(self):
        d_indices = [i for i, event in enumerate(self.trace) if event == 'D']
        for d_ind in d_indices:
            if 'E' not in self.trace[d_ind+1:d_ind+3]:
                assert False
        assert True

    def req_6(self):
        h_indices = [i for i, event in enumerate(self.trace) if event == 'H']
        if len(h_indices) >= 2:
            second_h_ind = h_indices[1]
            i_sequence = self.trace[second_h_ind+1:]
            consecutive_i_count = 0
            for event in i_sequence:
                if event == 'I':
                    consecutive_i_count += 1
                    if consecutive_i_count >= 3:
                        assert True
                        return
                else:
                    consecutive_i_count = 0
        assert False

    def req_7(self):
        a_indices = [i for i, event in enumerate(self.trace) if event == 'A']
        for i in range(len(a_indices) - 1):
            g_between = self.trace[a_indices[i]:a_indices[i+1]].count('G')
            if g_between > 3:
                assert False
        assert True

    def req_8(self):
        consecutive_y_count = 0
        for event in self.trace:
            if event == 'Y':
                consecutive_y_count += 1
                if consecutive_y_count > 2:
                    assert False
            else:
                consecutive_y_count = 0
        assert True

