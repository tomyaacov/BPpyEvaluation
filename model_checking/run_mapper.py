from dfs import *
from examples.dining_philosophers import *
from examples.hot_cold import *
from examples.ttt import *
import sys
from itertools import product

def main(args):
    example = args[0]

    if example == "hot_cold":
        N = int(args[1])
        M = int(args[2])
        set_bprogram(N, M)
        dfs = DFSBProgram([lambda: add_a()] + list(map((lambda n: lambda: add_b("COLD" + str(n))), range(M))) + [lambda: control2()],
                          SimpleEventSelectionStrategy(),
                          ["HOT"] + ["COLD" + str(i) for i in range(M)])

    if example == "dining_philosophers":
        N = int(args[1])
        set_dp_bprogram(int(args[1]))
        all_events = [BEvent(f"T{i}R") for i in range(N)] + \
                     [BEvent(f"T{i}L") for i in range(N)] + \
                     [BEvent(f"P{i}R") for i in range(N)] + \
                     [BEvent(f"P{i}L") for i in range(N)] + \
                     [BEvent(f"TS{i}") for i in range(N)] + \
                     [BEvent(f"RS{i}") for i in range(N)]
        dfs = DFSBProgram(list(map((lambda n: lambda: philosopher(n)), range(N))) +
                          list(map((lambda n: lambda: fork(n)), range(N))) +
                          [lambda: fork_eventually_released(0)] +
                          [lambda: semaphore()] +
                          list(map((lambda n: lambda: take_semaphore(n)), range(N))),
                          SimpleEventSelectionStrategy(),
                          [x.name for x in all_events])
    if example == "ttt":
        R = int(args[1])
        C = int(args[2])
        set_ttt_bprogram(R, C)
        any_x = [x(i, j) for i in range(R) for j in range(C)]
        any_o = [o(i, j) for i in range(R) for j in range(C)]
        move_events = any_x + any_o
        all_events = move_events + [BEvent('OWin'), BEvent('XWin'), BEvent('Draw')]
        LINES = [[(i, j) for j in range(C)] for i in range(R)] + [[(i, j) for i in range(R)] for j in range(C)] + [
            [(i, i) for i in range(R)]] + [[(i, R - i - 1) for i in range(R)]]
        x_lines = [[x(i, j) for (i, j) in line] for line in LINES]
        o_lines = [[o(i, j) for (i, j) in line] for line in LINES]
        dfs = DFSBProgram(list(map((lambda arg: lambda: square_taken(*arg)), product(range(R), range(C)))) +
                          [lambda: enforce_turns(), lambda: end_of_game(), lambda: detect_draw(), lambda: player_o(), lambda: player_x()] +
                          list(map((lambda line: lambda: detect_x_win(line)), x_lines)) +
                          list(map((lambda line: lambda: detect_x_win(line)), o_lines)),
                          SimpleEventSelectionStrategy(),
                          [x.name for x in all_events])

    init_s, visited = dfs.run()
    #DFSBProgram.save_graph(init_s, visited, "output/dfs.dot")
    print("number of events:", len(dfs.event_list))
    print("number of states:", len(visited))




if __name__ == "__main__":
    if len(sys.argv) < 2:
        main("dining_philosophers 2".split())
        #main("hot_cold 3 1".split())
        #main("ttt2 2 2".split())
    else:
        main(sys.argv[1:])





