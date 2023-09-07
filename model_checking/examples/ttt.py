from bppy import BEvent, b_thread, waitFor, request, block, BProgram, PrintBProgramRunnerListener, SimpleEventSelectionStrategy
data = "data"

def set_ttt_bprogram(n, m):
    global R, C, LINES, any_x, any_o, move_events, all_events, x_lines, o_lines, static_event
    R = n
    C = m
    static_event = {
        'OWin': BEvent('OWin'),
        'XWin': BEvent('XWin'),
        'draw': BEvent('Draw')
    }
    LINES = [[(i, j) for j in range(C)] for i in range(R)] + [[(i, j) for i in range(R)] for j in range(C)] + [
        [(i, i) for i in range(R)]] + [[(i, R - i - 1) for i in range(R)]]
    any_x = [x(i, j) for i in range(R) for j in range(C)]
    any_o = [o(i, j) for i in range(R) for j in range(C)]
    move_events = any_x + any_o
    all_events = move_events + list(static_event.values())
    x_lines = [[x(i, j) for (i, j) in line] for line in LINES]
    o_lines = [[o(i, j) for (i, j) in line] for line in LINES]


def x(row, col):
    return BEvent('X' + str(row) + str(col))


def o(row, col):
    return BEvent('O' + str(row) + str(col))




@b_thread
def square_taken(row, col):
    yield {waitFor: [x(row, col), o(row, col)]}
    yield {block: [x(row, col), o(row, col)]}

@b_thread
def fault_square_taken(row, col):
    if row == 2 and col == 2:
        good = False
        yield {waitFor: [x(row, col), o(row, col)], data: locals()}
        yield {block: [x(row, col)], data: locals()}
    else:
        good = True
        yield {waitFor: [x(row, col), o(row, col)], data: locals()}
        yield {block: [x(row, col), o(row, col)], data: locals()}


@b_thread
def enforce_turns():
    while True:
        yield {waitFor: any_x, block: any_o}
        yield {waitFor: any_o, block: any_x}


@b_thread
def end_of_game():
    yield {waitFor: list(static_event.values())}
    yield {block: all_events}


@b_thread
def detect_draw():
    for r in range(R):
        for c in range(C):
            yield {waitFor: move_events, data: locals()}
    yield {request: static_event['draw'], block: move_events}


@b_thread
def detect_x_win(line):
    for i in range(R):
        yield {waitFor: line, data: locals()}
    yield {request: static_event['XWin'], block: [e for e in all_events if e != static_event['XWin']]}


@b_thread
def detect_o_win(line):
    for i in range(R):
        yield {waitFor: line, data: locals()}
    yield {request: static_event['OWin'], block: [e for e in all_events if e != static_event['OWin']]}

# player O strategies:
# Add a third O to win
# Prevent a third X to not lose
# Preference to put O on center
# Win fork
# block X fork
# put O on corners
# put O on sides




# # player O strategy to add a third O to win
# @b_thread
# def add_third_o(line):
#     for i in range(R-1):  # check when we have different R
#         yield {waitFor: line}
#     yield {request: line, waitFor:  block: [m for m in any_o if m not in line]}


# player O strategy to prevent a third X
# @b_thread
# def prevent_third_x(xline, oline):
#     need_to_prevent = True
#     i = 0
#     while i < R-1:  # check when we have different R
#         e = yield {waitFor: xline + oline}
#         if e in oline:
#             need_to_prevent = False
#             break
#         else:
#             i += 1
#     if need_to_prevent:
#         yield {request: oline, block: [e for e in any_o if e not in oline]}


# Preference to put O on the center
# @b_thread
# def center_preference():
#     yield {request: o(1, 1), waitFor: [o(1, 1), x(1, 1)], block: [e for e in any_o if e != o(1, 1)]}
#     print("b")
#
#
# @b_thread
# def corner_preference():
#     yield {waitFor: [o(1, 1), x(1, 1)]}
#     o_corners_list = [o(0, 0), o(0, 2), o(2, 0), o(2, 2)]
#     x_corners_list = [x(0, 0), x(0, 2), x(2, 0), x(2, 2)]
#     for i in range(4):
#         print("a")
#         yield {request: o_corners_list, waitFor: o_corners_list + x_corners_list, block: [e for e in any_o if e not in o_corners_list]}

@b_thread
def player_o():
    while True:
        yield {request: any_o}


# simulate player X
@b_thread
def player_x():
    while True:
        yield {request: any_x}


if __name__ == "__main__":
    set_ttt_bprogram(4,4)
    bprog = BProgram(
        bthreads=[square_taken(i, j) for i in range(R) for j in range(C)]
                 + [enforce_turns(), end_of_game(), detect_draw()]
                 + [detect_x_win(line) for line in x_lines]
                 + [detect_o_win(line) for line in o_lines]
                 #+ [add_third_o(line) for line in o_lines]
                 #+ [prevent_third_x(xline, oline) for (xline, oline) in zip(x_lines, o_lines)]
                 + [player_o(), player_x()],
        event_selection_strategy=SimpleEventSelectionStrategy(),
        listener=PrintBProgramRunnerListener()
    )
    bprog.run()


