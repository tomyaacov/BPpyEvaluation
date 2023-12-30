import unittest

prompt = """
Event List:

- User Registration (Event A): A new user registers in the system.
- User Login (Event B): A user logs into their account.
- User Logout (Event C): A user logs out of their account.
- Create New Post (Event D): A user creates a new post on the platform.
- Edit Post (Event E): A user edits an existing post.
- Delete Post (Event F): A user deletes a post.
- Like Post (Event G): A user likes a post.
- Comment on Post (Event H): A user comments on a post.
- User Profile Update (Event I): A user updates their profile information.

Requirements List:

- Event A (User Registration) should occur before Event B (User Login).
- Event B (User Login) should be followed by Event C (User Logout).
- Event D (Create New Post) should occur after Event B (User Login) and before Event C (User Logout).
- Event E (Edit Post) and Event F (Delete Post) should not occur in succession. If E occurs, it should not be followed by F immediately.
- Event G (Like Post) and Event H (Comment on Post) should not occur in succession. If G occurs, it should not be followed by H immediately.
- Event D (Create New Post) should be followed by Event G (Like Post) or Event H (Comment on Post).
- After the second occurrence of Event I (User Profile Update), there should be a sequence of at least three consecutive Event D (Create New Post) events.
- There should be no more than 4 occurrences of Event E (Edit Post) between any two occurrences of Event B (User Login).
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 8

    def req_1(self):
        if "A" not in self.trace or "B" not in self.trace:
            assert False
        a_ind = self.trace.index('A')
        b_ind = self.trace.index('B')
        assert a_ind < b_ind

    def req_2(self):
        if "B" not in self.trace or "C" not in self.trace:
            assert False
        b_ind = self.trace.index('B')
        c_ind = self.trace.index('C')
        assert b_ind < c_ind

    def req_3(self):
        if "B" not in self.trace or "C" not in self.trace or "D" not in self.trace:
            assert False
        b_ind = self.trace.index('B')
        c_ind = self.trace.index('C')
        d_ind = self.trace.index('D')
        assert b_ind < d_ind < c_ind

    def req_4(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'E' and self.trace[i + 1] == 'F':
                assert False
        assert True

    def req_5(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'G' and self.trace[i + 1] == 'H':
                assert False
        assert True

    def req_6(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'D' and self.trace[i + 1] not in ['G', 'H']:
                assert False
        assert True

    def req_7(self):
        i_indices = [i for i, event in enumerate(self.trace) if event == 'I']
        if len(i_indices) >= 2:
            second_i_ind = i_indices[1]
            d_sequence = self.trace[second_i_ind+1:]
            consecutive_d_count = 0
            for event in d_sequence:
                if event == 'D':
                    consecutive_d_count += 1
                    if consecutive_d_count >= 3:
                        assert True
                        return
                else:
                    consecutive_d_count = 0
        assert False

    def req_8(self):
        b_indices = [i for i, event in enumerate(self.trace) if event == 'B']
        for i in range(len(b_indices) - 1):
            e_between = self.trace[b_indices[i]:b_indices[i+1]].count('E')
            if e_between > 4:
                assert False
        assert True




