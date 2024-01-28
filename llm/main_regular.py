#import openai
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

with open('files/intro_regular.txt', 'r') as f_intro:
    intro = f_intro.read()


prompt = intro.format(requirements=prompt)

print(prompt)

# completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
#                                           messages=[{"role": "user", "content": prompt}],
#                                           temperature=0)
# answer = completion.choices[0].message.content
# print(answer)
# with open("answers/regular/rs10", "w") as f:
#     f.write(answer)

with open("answers/regular/rs10", "r") as f:
    answer = f.read()

print(answer)

def get_function(answer):
    f_dict = {}
    exec(answer, globals(), f_dict)
    d = dict([(k, v) for k, v in f_dict.items()])
    f = None
    for k, v in d.items():
        if callable(v):
            f = v
            break
    return f


def clean_trace(trace):
    l = []
    for e in trace:
        if "A" in e:
            l.append("A")
        elif "B" in e:
            l.append("B")
        elif "C" in e:
            l.append("C")
        elif "D" in e:
            l.append("D")
        elif "E" in e:
            l.append("E")
        elif "F" in e:
            l.append("F")
        elif "G" in e:
            l.append("G")
        elif "H" in e:
            l.append("H")
        elif "I" in e:
            l.append("I")
        elif "J" in e:
            l.append("J")
        elif "K" in e:
            l.append("K")
        elif "L" in e:
            l.append("L")
        elif "M" in e:
            l.append("M")
        elif "N" in e:
            l.append("N")
        elif "O" in e:
            l.append("O")
        elif "P" in e:
            l.append("P")
        elif "Q" in e:
            l.append("Q")
        elif "R" in e:
            l.append("R")
        elif "S" in e:
            l.append("S")
        elif "T" in e:
            l.append("T")
        elif "U" in e:
            l.append("U")
        elif "V" in e:
            l.append("V")
        elif "W" in e:
            l.append("W")
        elif "X" in e:
            l.append("X")
        elif "Y" in e:
            l.append("Y")
        elif "Z" in e:
            l.append("Z")
    return l


n = 100
f = get_function(answer)
exec(answer)
if f is None:
    raise Exception("No function found")
results = [0] * Test(trace=[]).tests_num
for i in range(n):
    try:
        trace = f()
    except Exception as e:
        #print(e)
        continue
    #print(trace)
    trace = clean_trace(trace)
    test_obj = Test(trace=trace)
    for j in range(len(results)):
        try:
            test_obj.__getattribute__("req_" + str(j + 1))()
            results[j] += 1
        except AssertionError:
            pass

print("alignment of 100 sampled traces with requirements:")
print([x / n for x in results])
