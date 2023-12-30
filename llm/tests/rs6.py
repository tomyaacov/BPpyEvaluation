import unittest

prompt = """
Event List:

- Project Creation (Event A): A project is created by a project manager.
- Task Assignment (Event B): A project manager assigns a task to a team member.
- Task Completion (Event C): A team member completes a task.
- Task Review (Event D): The project manager reviews the completed task.
- Project Update (Event E): The project manager updates the project status.

Requirements List:

- Event A (Project Creation) should always be followed by Event B (Task Assignment).
- Event B (Task Assignment) should be followed by Event C (Task Completion) and then Event D (Task Review).
- Event D (Task Review) should be followed by Event E (Project Update).
- Event C (Task Completion) should not occur more than once in a sequence of events.
- If Event B (Task Assignment) occurs, it should be followed by Event C (Task Completion) before another Event B.
- Event E (Project Update) should occur after Event B (Task Assignment).
- Event B (Task Assignment) and Event D (Task Review) should not occur consecutively.
- Event A (Project Creation) should only occur once per project.
- After Event E (Project Update), there should be no more Event B (Task Assignment) until a new Project Creation (Event A) occurs.
"""


class Test(unittest.TestCase):

    def __init__(self, trace, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.trace = trace
        self.tests_num = 9

    def req_1(self):
        project_creation_indices = [i for i, event in enumerate(self.trace) if event == 'A']
        for i in range(len(project_creation_indices) - 1):
            next_event = self.trace[project_creation_indices[i] + 1]
            if next_event != 'B':
                assert False
        assert True

    def req_2(self):
        for i in range(len(self.trace) - 2):
            if self.trace[i] == 'B':
                next_event = self.trace[i + 1]
                next_next_event = self.trace[i + 2]
                if next_event != 'C' or next_next_event != 'D':
                    assert False
        assert True

    def req_3(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'D':
                next_event = self.trace[i + 1]
                if next_event != 'E':
                    assert False
        assert True

    def req_4(self):
        task_completion_count = 0
        for event in self.trace:
            if event == 'C':
                task_completion_count += 1
                if task_completion_count > 1:
                    assert False
            else:
                task_completion_count = 0
        assert True

    def req_5(self):
        b_allowed = True
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'B':
                assert b_allowed
                b_allowed = False
            elif self.trace[i] == 'C':
                b_allowed = True
        assert True

    def req_6(self):
        project_update_indices = [i for i, event in enumerate(self.trace) if event == 'E']
        for update_index in project_update_indices:
            task_assignment_indices = [i for i in range(update_index, len(self.trace)) if self.trace[i] == 'B']
            if not task_assignment_indices:
                assert False
        assert True

    def req_7(self):
        for i in range(len(self.trace) - 1):
            if self.trace[i] == 'B' and self.trace[i + 1] == 'D':
                assert False
        assert True

    def req_8(self):
        project_creation_indices = [i for i, event in enumerate(self.trace) if event == 'A']
        if len(project_creation_indices) > 1:
            assert False
        assert True

    def req_9(self):
        project_update_indices = [i for i, event in enumerate(self.trace) if event == 'E']
        for update_index in project_update_indices:
            task_assignment_indices = [i for i in range(update_index, len(self.trace)) if self.trace[i] == 'B']
            if task_assignment_indices:
                assert False
        assert True




