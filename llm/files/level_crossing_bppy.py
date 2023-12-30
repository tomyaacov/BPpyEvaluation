from bppy import *


# The railway sensor system dictates the exact event order: train approaching, entering, and then leaving. Also, there is no overlapping between successive train passages.
@b_thread
def railway_sensor():
    while True:
        yield {waitFor: BEvent("Approaching")}
        yield {waitFor: BEvent("Entering")}
        yield {waitFor: BEvent("Leaving")}


# The barriers are lowered when a train is approaching and then raised as soon as possible.
@b_thread
def barrier():
    while True:
        yield {waitFor: BEvent("Approaching")}
        yield {request: BEvent("Lower")}
        yield {request: BEvent("Raise")}


# A train may not enter while barriers are up.
@b_thread
def train():
    while True:
        yield {waitFor: BEvent("Lower"), block: BEvent("Entering")}
        yield {waitFor: BEvent("Raise")}

# The barriers may not be raised while a train is in the intersection zone. The intersection zone is the area between the approaching and leaving sensors.
