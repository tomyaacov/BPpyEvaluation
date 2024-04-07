import datetime
import csv
from bit_flipping_discrete import run_bit_flipping_discrete_bp_program
from bit_flipping_smt import run_bit_flipping_smt_bp_program

def init_statistics_file():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"statistics_{timestamp}.csv"
    return filename


def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--n", type=int, default=3, help="Number of rows"
    )
    parser.add_argument(
        "-m", "--m", type=int, default=3, help="Number of cols"
    )
    parser.add_argument(
        "-n_e", "--num_of_exp", type=int, default=3, help="The number of times to run the experiment"
    )
    args = parser.parse_args()
    return args.n, args.m, args.num_of_exp

def run_experiemnts(csvfile, n, m, number_of_experiments=1):

    # Init a dictionary to store n*m keys and the appropriate n,m value
    n_x_m_dict  = {}
    for n in range(2, n + 1):
        for m in range(2, m + 1):
            if n*m not in n_x_m_dict:
                n_x_m_dict[n*m] = (n,m)

    # Sort the dictionary by key - multiplication of n*m
    n_x_m_dict = {k: v for k, v in sorted(n_x_m_dict.items())}

    header = [
        "nXm",
        "(n,m)",
        "execution_time_discrete",
        "memory_usage_discrete",
        "execution_time_smt",
        "memory_usage_smt",
    ]

    writer = csv.writer(csvfile, delimiter=",")
    writer.writerow(header)
    print(",".join(header))

    execution_time_discrete_dict = {}
    memory_usage_discrete_dict = {}
    execution_time_smt_dict = {}
    memory_usage_smt_dict = {}

    for exp in range(number_of_experiments):
        for key in n_x_m_dict.keys():
                n,m = n_x_m_dict[key]
                execution_time_discrete,memory_usage_discrete = run_bit_flipping_discrete_bp_program( n, m )
                execution_time_smt, memory_usage_smt = run_bit_flipping_smt_bp_program(n, m)
                if key not in execution_time_discrete_dict:
                    execution_time_discrete_dict[key] = execution_time_discrete
                    memory_usage_discrete_dict[key] = memory_usage_discrete
                    execution_time_smt_dict[key] = execution_time_smt
                    memory_usage_smt_dict[key] = memory_usage_smt
                else:
                    execution_time_discrete_dict[key] += execution_time_discrete
                    memory_usage_discrete_dict[key] += memory_usage_discrete
                    execution_time_smt_dict[key] += execution_time_smt
                    memory_usage_smt_dict[key] += memory_usage_smt

    for key in n_x_m_dict.keys():
        execution_time_discrete_dict[key] /= number_of_experiments # average the execution time
        execution_time_discrete_dict[key] = 1000 * execution_time_discrete_dict[key] # From seconds to milliseconds
        # print(f"{key} Avg. Execution time discrete: ", execution_time_discrete_dict[key])

        memory_usage_discrete_dict[key] /= number_of_experiments  # average the memory usage,units in KB
        # print(f"{key} Avg. Memory usage discrete: ", memory_usage_discrete_dict[key])

        execution_time_smt_dict[key] /= number_of_experiments # average the execution time
        execution_time_smt_dict[key] = 1000 * execution_time_smt_dict[key] # From seconds to milliseconds
        # print(f"{key} Avg. Execution time smt: ", execution_time_smt_dict[key])

        memory_usage_smt_dict[key] /= number_of_experiments  # average the memory usage, units in KB
        # print(f"{key} Avg. Memory usage: smt", memory_usage_smt_dict[key])

        row = [key, n_x_m_dict[key], execution_time_discrete_dict[key], memory_usage_discrete_dict[key], execution_time_smt_dict[key], memory_usage_smt_dict[key]]
        writer.writerow(row)
        print(",".join([str(x) for x in row]))

if __name__ == '__main__':
    try:
        with open(init_statistics_file(), mode="w", newline="") as csvfile:
            current_datetime = datetime.datetime.now()
            n, m, num_of_exp = parse_arguments()
            run_experiemnts(csvfile, n, m, num_of_exp)
    except KeyboardInterrupt:
        # this code handles keyboard interrupt
        print("Keyboard interrupt")
    except IOError as e:
        print(f"An error occurred: {e}")