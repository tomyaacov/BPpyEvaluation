# import openai
import argparse
import importlib
import os

parser = argparse.ArgumentParser()
parser.add_argument("parameters", nargs="*", default=["rs1"])
args = parser.parse_args()
example = args.parameters[0]


with open(os.path.dirname(os.path.realpath(__file__)) + "/tests/" + example + ".py", "r") as f:
    exec(f.read())


# with open('secrets/openai_api_key', 'r') as f_api_key:
#     openai.api_key = f_api_key.read()

with open('files/intro_bppy.txt', 'r') as f_intro:
    intro = f_intro.read()
with open('files/hot_cold_bppy.py', 'r') as f_hot_cold:
    hot_cold = f_hot_cold.read()

prompt = intro.format(hot_cold=hot_cold, requirements=prompt)

print(prompt)

# completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
#                                           messages=[{"role": "user", "content": prompt}],
#                                           temperature=0)
# answer = completion.choices[0].message.content
# print(answer)
# with open("answers/bppy/rs10", "w") as f:
#     f.write(answer)

with open("answers/bppy/rs10", "r") as f:
    answer = f.read()

print(answer)


def get_functions(answer):
    f_dict = {}
    try:
        exec(answer, globals(), f_dict)
    except Exception as e:
        pass
        #print(e)
    d = dict([(k, v) for k, v in f_dict.items()])
    f = []
    for k, v in d.items():
        if isfunction(v) and v.__name__ == "wrapper":
            f.append(v)
    return f

from bppy import *
bthreads = get_functions(answer)
#print(bthreads)

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
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
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
print("alignment of 100 sampled traces with requirements:")
print([x / n for x in results])