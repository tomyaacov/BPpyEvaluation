from math import sqrt
from bppy import *
import bppy as bp
from constraints_generation import *
import timeit
import datetime
import csv
import random
import tracemalloc

random.seed(42)
x, y = Reals("x y")
found_solution_discrete = False
found_solution_solver = False
number_of_discrete_events = 0
number_of_equations = 0
x_y_events = []


def generate_x_y_events(x_y_events, delta_param):
    number_of_discrete_events = 0
    x_y_events.clear()
    x, y = -1.0, -1.0
    while x < 1.0:
        while y < 1.0:
            x_y_events.append(BEvent("set", {"x": x, "y": y}))
            y += delta_param
        y = -1.0
        x += delta_param
    return len(x_y_events)

def generate_x_y_events_sanity(x_y_events, delta_param):
    number_of_discrete_events = 0
    x_y_events.clear()
    x = -1.0
    while x < 1.0:
        x_y_events.append(BEvent("set", {"x": x}))
        x += delta_param
    # random.shuffle(x_y_events)
    return len(x_y_events)


def z3_point_between_triangle_and_circle():
    x, y = Reals("x y")
    solver = Solver()
    solver.add(And(y > (-1 / sqrt(3)) * x + (1 / sqrt(3)), x ** 2 + y ** 2 < 1))
    if solver.check() == sat:
        model = solver.model()
        solution_x = model[x].as_fraction()  # Retrieve the values of the variables
        solution_y = model[y].as_fraction()
        # print(f"x = {float(solution_x)}, y = {float(solution_y)}")
        return solution_x, solution_y


def print_line_equations(line_equations):
    for line_equation in line_equations:
        print(line_equation)


def check_equations(point, line_equations):
    for line_equation in line_equations:
        if line_equation.get_b >= 0:
            if (
                point.get_y()
                > line_equation.get_m() * point.get_x() + line_equation.get_b()
            ):
                if point.get_x() ** 2 + point.get_y() ** 2 < 1:
                    return True
                return
        else: # b < 0
            if ( point.get_y()
            < line_equation.get_m() * point.get_x() + line_equation.get_b()
            ):
                if point.get_x() ** 2 + point.get_y() ** 2 < 1:
                    return True
                return


def check_equation(x, y, line_equation, discrete_mode=True):
    val = ""
    if line_equation.get_type() == "y":
        if not is_almost_zero(line_equation.get_m()):
            if line_equation.get_b() >= 0:
                if y > (line_equation.get_m() * x + line_equation.get_b()):
                    val = (
                            f"{y} > {line_equation.get_m()} * {x} + "
                            + f"{line_equation.get_b()}"
                    )
            else: # b < 0
                if y < (line_equation.get_m() * x + line_equation.get_b()):
                    val = (
                            f"{y} < {line_equation.get_m()} * {x} + "
                            + f"{line_equation.get_b()}"
                    )
        '''else:  # we ignore the case of y=b from now on 
            if y < (line_equation.get_m() * x + line_equation.get_b()):
                val = (
                        f"{y} < {line_equation.get_m()} * {x} + "
                        + f"{line_equation.get_b()}"
                )
            else:  # M > 0
                if y < (line_equation.get_m() * x + line_equation.get_b()):
                    val = (
                        f"{y} < {line_equation.get_m()} * {x} + "
                        + f"{line_equation.get_b()}"
                    )
                    '''
    '''else:  # line_equation.get_type() == "x" # We ignore the case of X=b from now on
        if line_equation.get_x() >= 0:
            if x > line_equation.get_x():
                val = f"{x} > {line_equation.get_x()}"
        else:  # x1 < 0
            if x < line_equation.get_x():
                val = f"{x} < {line_equation.get_x()}"'''
    return val


def print_solution(str, event, m, b):
    solution_x = event[x].as_fraction()
    solution_y = event[y].as_fraction()
    # print(f"{str} = {float(solution_x)}, y = {float(solution_y)}")


"""
Solver event selection experiment bThreads
"""

count = 0


@bp.thread
def y_above_top_line_solver(m, b):
    global count
    y_above_top_line_solver = And(y > m * x + b)
    count = count + 1
    # if count % 1000 == 0:
    # print(f"y_above_top_line_solver: count={count}")
    yield bp.sync(request=y_above_top_line_solver)


@bp.thread
def y_below_top_line_solver(m, b):
    # print(f"x_y_below_line_solver: m={m}, b={b}")
    y_below_line_solver = And(y < m * x + b)
    yield bp.sync(request=y_below_line_solver)


@bp.thread
def y_above_b_solver(b):
    # print(f"y_above_b_solver: b={b}")
    y_above_b = And(y > b)
    yield bp.sync(request=y_above_b)


@bp.thread
def y_below_b_solver(b):
    # print(f"y_below_b_solver: b={b}")
    y_below_b = And(y < b)
    yield bp.sync(request=y_below_b)


@bp.thread
def x_above_x1_solver(x1):
    # print(f"x_above_x1_solver: x1={x1}")
    x_above_x1 = And(x > x1)
    yield bp.sync(request=x_above_x1)


@bp.thread
def x_below_x1_solver(x1):
    # print(f"x_below_x1_solver: x1={x1}")
    # x_below_x1 = And(x >= x1)
    x_below_x1 = And(x < x1)
    yield bp.sync(request=x_below_x1)


@bp.thread
def x_y_inside_circle_solver():
    x_y_outside_circle_constraint = And(x ** 2 + y ** 2 >= 1)
    yield bp.sync(block=x_y_outside_circle_constraint)


@bp.thread
def find_equation_for_solution_solver(line_equations, x, y):
    # x_y_in_range = And(x >= -1)
    # x_y_in_range = And(x >= -1, x <= 1, y >= -1, y <= 1)
    global found_solution_solver
    last_event = yield bp.sync(waitFor=true)
    found_solution_solver = True
    x = last_event[x].as_fraction()
    y = last_event[y].as_fraction()
    '''This code segment finds the equation for the found solution'''
    '''for line_equation in line_equations:
        solution = check_equation(x, y, line_equation, discrete_mode=False)
        if solution != "":
            # print(line_equation)
            print(f"Found solution solver: {solution}")
            break'''


@bp.thread
def generate_events_scenario(delta_param):
    requested_events = []
    x, y = -1.0, -1.0
    while x < 1.0:
        while y < 1.0:
            requested_events.append(BEvent("set", {"x": x, "y": y}))
            y += delta_param
        y = -1.0
        x += delta_param
    yield bp.sync(request=requested_events)

def sanity_thread_discrete_t1():
    global found_solution_discrete
    x_above_x0 = list(
        filter(lambda e: e.data["x"] > -0.4, x_y_events)
    )
    last_event = yield bp.sync(request=x_above_x0)
    print("Found solution: ", last_event.data["x"])
    found_solution_discrete = True

def sanity_thread_discrete_t2():
    x_below_x1 = EventSet(lambda e: e.data["x"] > -0.3)
    last_event = yield bp.sync(waitFor=All(), block=x_below_x1)

def init_bthreads_sanity():
    b_threads_list = []
    b_threads_list.append(sanity_thread_discrete_t1())
    b_threads_list.append(sanity_thread_discrete_t2())
    return b_threads_list

@bp.thread
def x_y_inside_circle_discrete():
    x_outside_of_circle = EventSet(lambda e: e.data["x"] ** 2 + e.data["y"] ** 2 >= 1)
    yield bp.sync(waitFor=All(), block=x_outside_of_circle)


@bp.thread
def y_above_top_line_discrete(m, b):
    # print(f"y_above_top_line_discrete: m={m}, b={b}")
    y_above_top_line_discrete_lst = list(
        filter(lambda e: e.data["y"] > (m * e.data["x"] + b), x_y_events)
    )
    # print("y_above_top_line_discrete: ", y_above_top_line_discrete_lst)
    last_event = yield bp.sync(request=y_above_top_line_discrete_lst, waitFor=All())


@bp.thread
def y_below_top_line_discrete(m, b):
    # print(f"y_below_top_line_discrete: m={m}, b={b}")
    y_below_top_line_discrete_lst = list(
        filter(lambda e: e.data["y"] < (m * e.data["x"] + b), x_y_events)
    )
    # print("y_below_top_line_discrete_lst: ", y_below_top_line_discrete_lst)
    yield bp.sync(request=y_below_top_line_discrete_lst, waitFor=All())


@bp.thread
def y_above_b_discrete(b):
    # print(f"y_above_b_discrete: b={b}")
    y_above_b_events_lst = list(filter(lambda e: e.data["y"] > b, x_y_events))
    yield bp.sync(request=y_above_b_events_lst, waitFor=All())


@bp.thread
def y_below_b_discrete(b):
    # print(f"y_below_b_discrete: b={b}")
    y_below_b_discrete_lst = list(filter(lambda e: e.data["y"] < b, x_y_events))
    yield bp.sync(request=y_below_b_discrete_lst, waitFor=All())


@bp.thread
def x_above_x1_discrete(x1):
    # print(f"x_above_x1_discrete: x1={x1}")
    x_above_x1_discrete_lst = list(filter(lambda e: e.data["x"] > x1, x_y_events))
    yield bp.sync(request=x_above_x1_discrete_lst, waitFor=All())


@bp.thread
def x_below_x1_discrete(x1):
    # print(f"x_below_x1_discrete: x1={x1}")
    x_below_x1_discrete_lst = list(filter(lambda e: e.data["x"] < x1, x_y_events))
    yield bp.sync(request=x_below_x1_discrete_lst, waitFor=All())


@bp.thread
def find_equation_for_solution_discrete(line_equations):
    global found_solution_discrete
    last_event = yield bp.sync( waitFor=All())
    found_solution_discrete = True
    x = last_event.data["x"]
    y = last_event.data["y"]
    # print("Found solution discrete x,y: ", x, y)
    '''for line_equation in line_equations: # This code segment finds the equation that matches the solution
        solution = check_equation(x, y, line_equation)
        if solution != "":
            # print(line_equation)
            print(f"Found solution discrete: {solution}")
            break'''


"""
Initialize the solver based example BProgram
"""


def solver_based_example(num_edges=3, radius=1, single_equation=False):
    global found_solution_solver
    line_equations = create_all_line_equations(
        n=num_edges, r=radius, single_equation=single_equation
    )
    # print("Finished creating the line_equations")
    # print_line_equations(line_equations)
    b_threads_list = initialize_bthreads_list(line_equations, discrete_mode=False)
    b_program = BProgram(
        bthreads=b_threads_list, event_selection_strategy=SMTEventSelectionStrategy()
    )
    b_program.run()
    # found_solution_solver = b_program.get_found_solution()
    # print(f"Solver based example found solution:{found_solution_solver}")


def initialize_bthreads_list(line_equations, discrete_mode=True):
    b_threads_list = []

    if discrete_mode:
        b_threads_list.append(x_y_inside_circle_discrete())
    else:
        b_threads_list.append(x_y_inside_circle_solver())

    for line_equation in line_equations:
        if line_equation.get_type() == "y":
            if not is_almost_zero(line_equation.get_m()): #  y = mx + b
                if line_equation.get_b() >= 0: #  y = mx + b , b >= 0
                    if discrete_mode:
                        b_threads_list.append(y_above_top_line_discrete(line_equation.get_m(), line_equation.get_b()))
                    else:
                        b_threads_list.append(y_above_top_line_solver(line_equation.get_m(), line_equation.get_b()))
                else: # y = mx + b , b < 0
                    if discrete_mode:
                        b_threads_list.append(y_below_top_line_discrete(line_equation.get_m(), line_equation.get_b()))
                    else:
                        b_threads_list.append(y_below_top_line_solver(line_equation.get_m(), line_equation.get_b()))
            '''else:  we ignore the case of y=b from now on 
                if line_equation.get_b() > 0: # b > 0
                    if discrete_mode:
                        b_threads_list.append(
                            y_above_top_line_discrete(
                                line_equation.get_m(), line_equation.get_b()
                            )
                        )
                    else: # solver mode
                        b_threads_list.append(
                            y_above_top_line_solver(
                                line_equation.get_m(), line_equation.get_b()
                            )
                        )
                else:  # b < 0
                    if discrete_mode:
                        b_threads_list.append(
                            y_below_top_line_discrete(
                                line_equation.get_m(), line_equation.get_b()
                            )
                        )
                    else:
                        b_threads_list.append(
                            y_below_line_solver(
                                line_equation.get_m(), line_equation.get_b()
                            )
                        )
                        '''
        '''else:  # line_equation.get_type() == "x" # We ignore the case of X=b from now on
            if line_equation.get_x() >= 0:
                if discrete_mode:
                    b_threads_list.append(x_above_x1_discrete(line_equation.get_x()))
                else:
                    b_threads_list.append(x_above_x1_solver(line_equation.get_x()))
            else:  # x1 < 0
                if discrete_mode:
                    b_threads_list.append(x_below_x1_discrete(line_equation.get_x()))
                else:
                    b_threads_list.append(x_below_x1_solver(line_equation.get_x()))
            '''
    if discrete_mode:
        b_threads_list.append(find_equation_for_solution_discrete(line_equations))
    else:
        b_threads_list.append(find_equation_for_solution_solver(line_equations, x, y))

    return b_threads_list


"""
Initialize the discrete based example BProgram
"""


def discrete_event_example(
    num_edges=3, radius=1, delta_param=0.1, single_equation=False
):
    global found_solution_discrete
    global x_y_events
    global number_of_discrete_events
    global number_of_equations
    number_of_discrete_events = generate_x_y_events(x_y_events, delta_param)
    line_equations = create_all_line_equations(n=num_edges,
                                               r=radius,
                                               single_equation=single_equation)
    # print_line_equations(line_equations)
    number_of_equations = len(line_equations)
    # Change if we want sanity test
    b_threads_list = initialize_bthreads_list(line_equations, delta_param)
    # b_threads_list = init_bthreads_sanity()
    b_program = BProgram(
        bthreads=b_threads_list, event_selection_strategy=SimpleEventSelectionStrategy()
    )
    b_program.run()
    # print(f"Discrete event example found solution:{found_solution_discrete}")


def init_statistics_file():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"statistics_{timestamp}.csv"
    return filename


def tracemalloc_stop():
    snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()
    total_memory = sum(stat.size for stat in snapshot.statistics("filename"))
    memory_usage = total_memory / 1024 / 1024
    return memory_usage

def init_global_parameters():
    global found_solution_discrete
    found_solution_discrete = False
    global found_solution_solver
    found_solution_solver = False
    global number_of_discrete_events
    number_of_discrete_events = 0
    global number_of_equations
    number_of_equations = 0
    global x_y_events
    x_y_events = []

def run_experiments(csvfile, start_n, end_n, delta_param, number_of_experiments, single_equation=False,
                    end_time_global=None):
    global delta
    delta_reduction_divider = 2
    header = [
        "num_of_edges",
        "num_of_equations",
        "delta_param",
        "number_of_events",
        "execution_time_discrete",
        "memory_usage_discrete",
        "execution_time_solver",
        "memory_usage_solver",
    ]
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerow(header)
    print(",".join(header[:1] + header[4:]))

    # We initialize the overall statistics array to 0
    # The elements where i< start_n are not relevant for the experiment
    # and thier sum will remain 0
    execution_time_discrete_arr = [0.0] * end_n
    memory_usage_discrete_arr = [0.0] * end_n
    execution_time_solver_arr = [0.0] * end_n
    memory_usage_solver_arr = [0.0] * end_n
    delta_arr = [float('inf')] * end_n
    number_of_discrete_events_arr = [0] * end_n
    number_of_equations_arr = [0] * end_n

    for m in range(number_of_experiments):
        for n in range(start_n, end_n):
            delta = delta_param
            init_global_parameters()
            tracemalloc.start()
            start_time = timeit.default_timer()
            discrete_event_example(num_edges=n, radius=1, delta_param=delta, single_equation=single_equation)

            while not found_solution_discrete:
                init_global_parameters()
                delta = delta / delta_reduction_divider
                discrete_event_example(num_edges=n, radius=1, delta_param=delta,
                                   single_equation=single_equation)

            end_time = timeit.default_timer()
            execution_time_discrete = end_time - start_time
            memory_usage_discrete = tracemalloc_stop()

            # Documenting the results
            execution_time_discrete_arr[n] += execution_time_discrete
            memory_usage_discrete_arr[n] += memory_usage_discrete
            if number_of_discrete_events > number_of_discrete_events_arr[n]:
                number_of_discrete_events_arr[n] = number_of_discrete_events
            if delta < delta_arr[n]:
                delta_arr[n] = delta
            number_of_equations_arr[n] = number_of_equations
            # print("Finished discrete based example")

            # print("Started solver based example")
            tracemalloc.start()
            start_time_solver = timeit.default_timer()
            solver_based_example(num_edges=n, radius=1, single_equation=single_equation)
            end_time_solver = timeit.default_timer()

            execution_time_solver = end_time_solver - start_time_solver
            memory_usage_solver = tracemalloc_stop()
            execution_time_solver_arr[n] += execution_time_solver
            memory_usage_solver_arr[n] += memory_usage_solver
            # print("---- Finished experiment for edge: n=" + str(n) + " ----")
        # print("=================================================")
        # print("====== Finished experiment iteration (m= " + str(m) + ") =====")
        # print("=================================================")


    # Calculating the average results and writing them to the csv file
    for n in range(start_n, end_n):
        execution_time_discrete_arr[n] /= number_of_experiments
        memory_usage_discrete_arr[n] /= number_of_experiments
        execution_time_solver_arr[n] /= number_of_experiments
        memory_usage_solver_arr[n] /= number_of_experiments

        row = [
            n,
            # number_of_equations_arr[n],
            # delta_arr[n],
            # number_of_discrete_events_arr[n],
            execution_time_discrete_arr[n],
            memory_usage_discrete_arr[n],
            execution_time_solver_arr[n],
            memory_usage_solver_arr[n],
        ]
        writer.writerow(row)
        print(",".join([str(x) for x in row]))
        # print("Finished solver based example")


# the following method parses the command line arguments
# first argument - n_0 - start number of edges
# second argument - n_m - Max number of edges
# third argument - delta - the delta parameter
# fourth argument - single_equation - boolean value that indicates whether to use a single equation or multiple equations
def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n_0", "--start_n", type=int, default=4, help="start number of edges"
    )
    parser.add_argument(
        "-n_m", "--end_n", type=int, default=10, help="Max number of edges"
    )
    parser.add_argument(
        "-d", "--delta_param", type=float, default=1.0, help="delta parameter"
    )
    parser.add_argument(
        "-s",
        "--single_equation",
        action="store_true",
        default=False,
        help="single equation or multiple equations",
    )
    parser.add_argument(
        "-n_e", "--num_of_exp", type=int, default=2, help="The number of time to run the experiment"
    )
    args = parser.parse_args()
    return args.start_n, args.end_n, args.delta_param, args.num_of_exp, args.single_equation


if __name__ == "__main__":
    # discrete_event_example(1000, 1, 0.1)
    # solver_based_example(1000, 1)
    try:
        with open(init_statistics_file(), mode="w", newline="") as csvfile:
            current_datetime = datetime.datetime.now()
            # print("Current Date and Time =", current_datetime)
            start_n, end_n, delta_param, num_of_exp, single_equation = parse_arguments()
            # print(f"start_n={start_n}, end_n={end_n}, delta_param={delta_param}, num_of_exp={num_of_exp}, single_equation={single_equation}")
            run_experiments(csvfile, start_n, end_n, delta_param, num_of_exp, single_equation)
    except KeyboardInterrupt:
        # this code handles keyboard interrupt
        print("Keyboard interrupt")
    except IOError as e:
        print(f"An error occurred: {e}")
