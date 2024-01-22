from bp_model_check import ModelChecker
from examples.dining_philosophers import *
from examples.hot_cold import *
from examples.ttt import *
import sys
from itertools import product

def main(args):
    example = args[0]

    if example == "hot_cold1":
        N = int(args[1])
        M = int(args[2])
        set_bprogram(N, M)
        mc = ModelChecker(["HOT"] + ["COLD" + str(i) for i in range(M)],
                          [lambda: add_a()] + list(map((lambda n: lambda: add_b("COLD" + str(n))), range(M))) + [lambda: control()],
                          ["adda"] + ["addb"+str(i) for i in range(M)] + ["control"])
        spec = "G (F must_finish = FALSE)"
        bmc_length = N+5
    elif example == "hot_cold2":
        N = int(args[1])
        M = int(args[2])
        set_bprogram(N, M)
        mc = ModelChecker(["HOT"] + ["COLD" + str(i) for i in range(M)],
                          [lambda: add_a()] + list(map((lambda n: lambda: add_b("COLD" + str(n))), range(M))) + [lambda: control2()],
                          ["adda"] + ["addb"+str(i) for i in range(M)] + ["control"])
        spec = "G (F must_finish = FALSE)"
        bmc_length = N + 5
    elif example == "dining_philosophers1":
        N = int(args[1])
        set_dp_bprogram(int(args[1]))
        all_events = [BEvent(f"T{i}R") for i in range(N)] + \
                 [BEvent(f"T{i}L") for i in range(N)] + \
                 [BEvent(f"P{i}R") for i in range(N)] + \
                 [BEvent(f"P{i}L") for i in range(N)]
        mc = ModelChecker([x.name for x in all_events],
                          list(map((lambda n: lambda: philosopher(n)), range(N))) +
                          list(map((lambda n: lambda: fork(n)), range(N))) +
                          [lambda: fork_eventually_released(0)],
                          ["p" + str(i) for i in range(N)] +
                          ["f" + str(i) for i in range(N)] +
                          ["f0r"]
                          )
        spec = "G (!(event = DONE))"
        bmc_length = 10
    elif example == "dining_philosophers2":
        N = int(args[1])
        set_dp_bprogram(int(args[1]))
        all_events = [BEvent(f"T{i}R") for i in range(N)] + \
                     [BEvent(f"T{i}L") for i in range(N)] + \
                     [BEvent(f"P{i}R") for i in range(N)] + \
                     [BEvent(f"P{i}L") for i in range(N)] + \
                     [BEvent(f"TS{i}") for i in range(N)] + \
                     [BEvent(f"RS{i}") for i in range(N)]
        mc = ModelChecker([x.name for x in all_events],
                          list(map((lambda n: lambda: philosopher(n)), range(N))) +
                          list(map((lambda n: lambda: fork(n)), range(N))) +
                          [lambda: fork_eventually_released(0)] +
                          [lambda: semaphore()] +
                          list(map((lambda n: lambda: take_semaphore(n)), range(N))),
                          ["p" + str(i) for i in range(N)] +
                          ["f" + str(i) for i in range(N)] +
                          ["f0r"] +
                          ["s"] +
                          ["ts" + str(i) for i in range(N)])
        spec = "G (!(event = DONE))"
        bmc_length = 10
    elif example == "ttt1":
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
        mc = ModelChecker([x.name for x in all_events],
                          list(map((lambda arg: lambda: fault_square_taken(*arg)), product(range(R), range(C)))) +
                          [lambda: enforce_turns(), lambda: end_of_game(), lambda: detect_draw(), lambda: player_o(), lambda: player_x()] +
                          list(map((lambda line: lambda: detect_x_win(line)), x_lines)) +
                          list(map((lambda line: lambda: detect_x_win(line)), o_lines)),
                            ["st" + str(i) + str(j) for i in range(R) for j in range(C)] +
                            ["enforce_turns", "end_of_game", "detect_draw", "player_o", "player_x"] +
                            ["xwin" + str(i) for i in range(len(x_lines))] +
                            ["owin" + str(i) for i in range(len(o_lines))]
                            )
        spec = "F ((event = OWin) | (event = XWin) | (event = Draw))"
        bmc_length = R*C + 5
    elif example == "ttt2":
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
        mc = ModelChecker([x.name for x in all_events],
                          list(map((lambda arg: lambda: square_taken(*arg)), product(range(R), range(C)))) +
                          [lambda: enforce_turns(), lambda: end_of_game(), lambda: detect_draw(), lambda: player_o(), lambda: player_x()] +
                          list(map((lambda line: lambda: detect_x_win(line)), x_lines)) +
                          list(map((lambda line: lambda: detect_x_win(line)), o_lines)),
                            ["st" + str(i) + str(j) for i in range(R) for j in range(C)] +
                            ["enforce_turns", "end_of_game", "detect_draw", "player_o", "player_x"] +
                            ["xwin" + str(i) for i in range(len(x_lines))] +
                            ["owin" + str(i) for i in range(len(o_lines))]
                            )
        spec = "F ((event = OWin) | (event = XWin) | (event = Draw))"
        bmc_length = R*C + 5


    # spec = prop.ag(prop.af(prop.atom(("bt0.must_finish = FALSE"))))
    print("number of events:", len(mc.event_list))
    bmc_flag = args[-1] == "1"
    result, explanation = mc.check(spec, debug=True, find_counterexample=False, bmc=bmc_flag, bmc_length=bmc_length)
    print(result)
    if not result and explanation is not None:
        print("violation event trace:")
        print(explanation)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        #main("dining_philosophers1 2 0 1".split())
        main("hot_cold1 3 1 0".split())
        #main("ttt2 2 2 0".split())
    else:
        main(sys.argv[1:])
        # for i in [10, 20, 30]:
        #     for j in range(1, 4):
        #         print("-"*80)
        #         print("Example:", "hot_cold1", i, j)
        #         args = ["hot_cold1", i, j]
        #         main(args)
        #         print("-" * 80)
        #         print("Example:", "hot_cold2", i, j)
        #         args = ["hot_cold2", i, j]
        #         main(args)
        # for i in [2, 3]:
        #     print("-" * 80)
        #     print("Example:", "dining_philosophers1", i)
        #     args = ["dining_philosophers1", i]
        #     main(args)
        #     print("-" * 80)
        #     print("Example:", "dining_philosophers2", i)
        #     args = ["dining_philosophers2", i]
        #     main(args)




