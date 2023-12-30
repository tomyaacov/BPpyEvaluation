from bppy import *


# When the system loads, do 'HOT' three times.
@b_thread
def add_hot():
    for i in range(3):
        yield {request: BEvent("HOT")}


# When the system loads, do 'COLD' three times.
@b_thread
def add_cold():
    for i in range(3):
        yield {request: BEvent("COLD")}


# Prevent 'HOT' from being executed consecutively.
@b_thread
def prevent_consecutive_hot():
    while True:
        yield {waitFor: BEvent("HOT")}
        yield {block: BEvent("HOT"), waitFor: BEvent("COLD")}