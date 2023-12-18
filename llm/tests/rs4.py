import unittest

prompt = """
Event List:

- Email Sent (Event A): A user sends an email to another user.
- Email Received (Event B): A user receives an email from another user.
- Email Read (Event C): A user marks an email as read.
- Email Deleted (Event D): A user deletes an email.
- Email Forwarded (Event E): A user forwards an email to another user.
- Email Reply (Event F): A user replies to an email.
- Attachment Downloaded (Event G): A user downloads an attachment from an email.
- Email Draft Saved (Event H): A user saves an email as a draft.
- Email Sent Error (Event I): An error occurs while trying to send an email.
- Email Spam Marked (Event J): A user marks an email as spam.
- Email Filtered (Event K): An email is automatically moved to a specific folder based on filters.

Requirements List:

- Event A (Email Sent) should always be followed by Event B (Email Received).
- Event C (Email Read) should occur after Event B (Email Received) if the email is marked as read.
- Event D (Email Deleted) should occur after Event B (Email Received) or Event H (Email Draft Saved).
- Event E (Email Forwarded) should occur after Event B (Email Received).
- Event F (Email Reply) should occur after Event B (Email Received).
- Event G (Attachment Downloaded) can occur after Event B (Email Received) or Event F (Email Reply).
- Event I (Email Sent Error) should occur when there is an error while sending an email, and it should be followed by at least one of the following events within the next two events: Event A (Email Sent), Event H (Email Draft Saved), or Event F (Email Reply).
- Event J (Email Spam Marked) should occur when a user marks an email as spam, and it should be followed by Event K (Email Filtered) within the next event if the email was marked as spam.
- Event K (Email Filtered) can occur automatically based on predefined filters. If Event K occurs, it should be followed by Event D (Email Deleted) within the next two events if the filtered email was marked as spam. If the filtered email was not marked as spam, it should be followed by Event C (Email Read) within the next two events.
- No more than 5 consecutive Event D (Email Deleted) events should occur in a row.
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 10

    def req_1(self):
        self.assertIn('A', self.trace)
        self.assertIn('B', self.trace)
        a_index = self.trace.index('A')
        b_index = self.trace.index('B')
        self.assertLess(a_index, b_index)

    def req_2(self):
        if 'B' in self.trace and 'C' in self.trace:
            b_index = self.trace.index('B')
            c_index = self.trace.index('C')
            self.assertLess(b_index, c_index)

    def req_3(self):
        if 'B' in self.trace and 'D' in self.trace:
            b_index = self.trace.index('B')
            d_index = self.trace.index('D')
            self.assertLess(b_index, d_index)
        if 'H' in self.trace and 'D' in self.trace:
            h_index = self.trace.index('H')
            d_index = self.trace.index('D')
            self.assertLess(h_index, d_index)

    def req_4(self):
        if 'B' in self.trace and 'E' in self.trace:
            b_index = self.trace.index('B')
            e_index = self.trace.index('E')
            self.assertLess(b_index, e_index)

    def req_5(self):
        if 'B' in self.trace and 'F' in self.trace:
            b_index = self.trace.index('B')
            f_index = self.trace.index('F')
            self.assertLess(b_index, f_index)

    def req_6(self):
        if 'B' in self.trace and 'G' in self.trace:
            b_index = self.trace.index('B')
            g_index = self.trace.index('G')
            self.assertLess(b_index, g_index)
        if 'F' in self.trace and 'G' in self.trace:
            f_index = self.trace.index('F')
            g_index = self.trace.index('G')
            self.assertLess(f_index, g_index)

    def req_7(self):
        if 'I' in self.trace:
            i_index = self.trace.index('I')
            subsequent_events = self.trace[i_index + 1:i_index + 3]
            self.assertTrue(any(event in subsequent_events for event in ['A', 'H', 'F']))

    def req_8(self):
        if 'J' in self.trace:
            j_index = self.trace.index('J')
            self.assertIn('K', self.trace[j_index + 1:j_index + 2])

    def req_9(self):
        if 'K' in self.trace:
            k_index = self.trace.index('K')
            subsequent_events = self.trace[k_index + 1:k_index + 3]
            if 'J' in self.trace[k_index - 1:k_index]:
                self.assertIn('D', subsequent_events)
            else:
                self.assertIn('C', subsequent_events)

    def req_10(self):
        consecutive_d_count = 0
        for event in self.trace:
            if event == 'D':
                consecutive_d_count += 1
                if consecutive_d_count > 5:
                    assert False
            else:
                consecutive_d_count = 0
        assert True




