from bppy import *

data = "data"

@b_thread
def user_request():
    while True:
        yield {request: [BEvent("coin"), BEvent("button")]}


@b_thread
def return_coffee():
    while True:
        yield {waitFor: BEvent("button")}
        yield {request: [BEvent("coffee"), BEvent("not_enough")], block: [BEvent("coin")]}

@b_thread
def count():
    n = 0
    while True:
        if n >= 5:
            b = [BEvent("coin"), BEvent("not_enough")]
        elif n >= 2:
            b = [BEvent("not_enough")]
        else:
            b = [BEvent("coffee")]
        e = yield {waitFor: [BEvent("coin"), BEvent("coffee")], block: b, data: {"n": n}}
        if e == "coin":
            n += 1
        else:
            n -= 2

def bug1(): # if n reaches 5, adds a coin, then go back 2 and do button
    pass

# extensions:
# other drinks (with different price)
# different max n
# different coins (1, 2 , 5)

# bug - fifth coin does not counted.

from lstar_dfs import run
from bp_modules import *

event_list = ["button", "coin", "coffee", "not_enough"]
bt_list = []
bt_list.append(bthread_to_module(lambda : user_request(), "user_request", event_list))
bt_list.append(bthread_to_module(lambda: return_coffee(), "return_coffee", event_list))
bt_list.append(bthread_to_module(lambda: count(), "_count", event_list))

run(bt_list, event_list, "b.dot")





