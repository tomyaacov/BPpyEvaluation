import openai
from tests.lc import Test
from tests.lc import prompt as requirements

with open('secrets/openai_api_key', 'r') as f_api_key:
    openai.api_key = f_api_key.read()

intro = """
Consider the following system requirements that controls hot and cold water taps, whose output flows are mixed:

Events: HOT, COLD

Requirements:
1. Do 'HOT' three times.
2. Do 'COLD' three times.
3. Prevent 'HOT' from being executed consecutively.

The following is a code that satisfies the requirements:

import random

def f():
    possible_events = ["HOT", "COLD"]
    trace = []
    while trace.count("HOT") < 3 or trace.count("COLD") < 3:
        current_possible_events = possible_events
        if trace.count("HOT") >= 3:
            current_possible_events = [x for x in current_possible_events if x != "HOT"]
        if trace.count("COLD") >= 3:
            current_possible_events = [x for x in current_possible_events if x != "COLD"]
        if len(trace) > 0 and trace[-1] == "HOT":
            current_possible_events = [x for x in current_possible_events if x != "HOT"]

        if len(current_possible_events) == 0:
            break
        else:
            trace.append(random.choice(current_possible_events))
    return trace

Note that the function is non-deterministic and may return different traces each time it is called. This is to allow any trace which satisfies the system requirements to be returned.

Based on the following desired events and requirements, build a function that satisfies them.

The following is a system of a controller for a gate at a railway crossing - an intersection between a railway line and a road at the same level.

Events: Approaching, Entering, Leaving, Lower, Raise

Requirements:

1. When a train passes, the sensor system activates the exact event order: approaching, entering, and leaving.
2. The barriers are lowered when a train approaches and then raised.
3. A train may not enter while barriers are raised.
4. The barriers may not be raised while a train is passing, i.e. it approached but did not leave.


the list returned should be non-deterministic and should be able to generate a different list of
events each time it is called. That is to represent a different run of the system each time. Additionally, the function should
terminate.

Please answer with the code only and without any additional text.
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
# with open("answers/regular/lc", "w") as f:
#     f.write(answer)

# with open("answers/regular/lc", "r") as f:
#     answer = f.read()
#
# print(answer)
#
# def get_function(answer):
#     f_dict = {}
#     exec(answer, globals(), f_dict)
#     d = dict([(k, v) for k, v in f_dict.items()])
#     f = None
#     for k, v in d.items():
#         if callable(v):
#             f = v
#             break
#     return f
#
# n = 100
# f = get_function(answer)
# exec(answer)
# if f is None:
#     raise Exception("No function found")
# results = [0] * Test(trace=[]).tests_num
# for i in range(n):
#     try:
#         trace = f()
#     except Exception as e:
#         print(e)
#         continue
#     print(trace)
#     test_obj = Test(trace=trace)
#     for j in range(len(results)):
#         try:
#             test_obj.__getattribute__("req_" + str(j + 1))()
#             results[j] += 1
#         except AssertionError:
#             pass
# print([x / n for x in results])

