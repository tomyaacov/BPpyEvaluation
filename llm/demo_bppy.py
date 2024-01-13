import openai
from tests.lc import Test
from tests.lc import prompt as requirements

with open('secrets/openai_api_key', 'r') as f_api_key:
    openai.api_key = f_api_key.read()

intro = """
Behavioral Programming (BP) is a modeling paradigm designed to allow developers to specify the behavior of reactive systems incrementally and intuitively in a way that is aligned with system requirements.
A BP program, is defined by a set of b-threads representing the different behaviors of the system.
The protocol involves each b-thread issuing a statement before selecting every system-generated event.
In the statement, the b-thread declares which events it requests, waits for (but does not request), and blocks (forbids from happening).
After submitting the statement, the b-thread is paused.
When all b-threads have submitted their statements, we say the b-program has reached a synchronization point (yield point).
Then, an event arbiter picks a single event that has been requested but not blocked.
The b-program then resumes all b-threads that either requested or waited for the chosen event, leaving others paused, and their existing statements are carried forward to the next yield point.
This process is repeated throughout the program's execution, terminating when there are no requested non-blocked events.

For instance, given the consider the following system requirements that controls hot and cold water taps, whose output flows are mixed:

Events: HOT, COLD

Requirements:
1. Do 'HOT' three times.
2. Do 'COLD' three times.
3. Prevent 'HOT' from being executed consecutively.

The following is a b-program that satisfies the requirements:

@b_thread
def req_1():
    for i in range(3):
        yield {request: BEvent("HOT")}

@b_thread
def req_2():
    for i in range(3):
        yield {request: BEvent("COLD")}

@b_thread
def req_3():
    while True:
        yield {waitFor: BEvent("HOT")}
        yield {block: BEvent("HOT"), waitFor: BEvent("COLD")}

Based on the following desired events and requirements, build a b-program that satisfies them.

The following is a system of a controller for a gate at a railway crossing - an intersection between a railway line and a road at the same level.

Events: Approaching, Entering, Leaving, Lower, Raise

Requirements:

1. When a train passes, the sensor system activates the exact event order: approaching, entering, and leaving.
2. The barriers are lowered when a train is approaching and then raised.
3. A train may not enter while barriers are raised.
4. The barriers may not be raised while a train is passing, i.e. it approached but did not leave.

Create a separate b-thread for each requirement. Avoid including any extra keys in yield statements beyond request, waitFor, and block. Please answer with the code only and without any additional text.
"""

# print(intro)
# prompt = intro.format(requirements=requirements)
prompt = intro
print(prompt)

completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                          messages=[{"role": "user", "content": prompt}],
                                          temperature=0)
answer = completion.choices[0].message.content
print(answer)
# with open("answers/bppy/lc", "w") as f:
#     f.write(answer)
#
# with open("answers/bppy/lc", "r") as f:
#     answer = f.read()
#
# print(answer)

# answer = """
# @b_thread
# def r1():  # train approaching, entering, and then leaving
#     while True:
#         yield {request: BEvent("Approaching")}
#         yield {request: BEvent("Entering")}
#         yield {request: BEvent("Leaving")}
#
# @b_thread
# def r2():  # The barriers are lowered when a train is approaching and then raised as soon as possible.
#     while True:
#         yield {waitFor: BEvent("Approaching")}
#         yield {request: BEvent("Lower")}
#         yield {request: BEvent("Raise")}
#
# @b_thread
# def r3():  # A train may not enter while barriers are up.
#     while True:
#         yield {waitFor: BEvent("Lower"), block: BEvent("Entering")}
#         yield {waitFor: BEvent("Raise")}
#
# @b_thread
# def r4():  # The barriers may not be raised while a train is in the intersection zone.
#     while True:
#         yield {waitFor: BEvent("Approaching")}
#         yield {waitFor: BEvent("Leaving"), block: BEvent("Raise")}
# """
#
def get_functions(answer):
    f_dict = {}
    try:
        exec(answer, globals(), f_dict)
    except Exception as e:
        print(e)
    d = dict([(k, v) for k, v in f_dict.items()])
    f = []
    for k, v in d.items():
        if isfunction(v) and v.__name__ == "wrapper":
            f.append(v)
    return f

from bppy import *
bthreads = get_functions(answer)
print(bthreads)

class EvaluatorListener(PrintBProgramRunnerListener):

    def starting(self, b_program):
        self.events = []

    def ended(self, b_program):
        pass

    def event_selected(self, b_program, event):
        self.events.append(event.name)
        if len(self.events) == 20:
            raise TimeoutError()

def init_bprogram():
    eval = EvaluatorListener()
    return BProgram(bthreads=[x() for x in bthreads],
                    event_selection_strategy=SimpleEventSelectionStrategy(),
                    listener=eval)


n = 100
results = [0] * Test(trace=[]).tests_num
for i in range(n):
    try:
        bprog = init_bprogram()
        bprog.run()
    except TimeoutError:
        pass
    trace = bprog.listener.events
    #print(trace)
    test_obj = Test(trace=trace)
    for j in range(len(results)):
        try:
            test_obj.__getattribute__("req_" + str(j + 1))()
            results[j] += 1
        except AssertionError:
            pass
print([x / n for x in results])

