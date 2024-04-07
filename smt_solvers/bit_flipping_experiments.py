import math

from bppy import BEvent
import itertools
import bppy as bp
import tracemalloc
import datetime
import csv
from bit_flipping_discrete import run_bit_flipping_discrete_bp_program
def init_statistics_file():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"statistics_{timestamp}.csv"
    return filename

def run_experiemnts(csvfile, max_n, max_m, number_of_experiments=1):


    # Init a dictionary to store n*m keys and the appropriate n,m value
    n_x_m_dict  = {}
    for n in range(2, max_n + 1):
        for m in range(2, max_m + 1):
            if n*m not in n_x_m_dict:
                n_x_m_dict[n*m] = (n,m)

    # Sort the dictionary by key - multiplication of n*m
    n_x_m_dict = {k: v for k, v in sorted(n_x_m_dict.items())}

    header = [
        "nXm",
        "(n,m)",
        "execution_time_discrete",
        "memory_usage_discrete",
        "execution_time_solver",
        "memory_usage_solver",
    ]

    writer = csv.writer(csvfile, delimiter=",")
    writer.writerow(header)
    print(",".join(header))

    execution_time_discrete_dict = {}
    memory_usage_discrete_dict = {}

    for exp in range(number_of_experiments):
        for key in n_x_m_dict.keys():
                n,m = n_x_m_dict[key]
                execution_time_discrete,memory_usage_discrete = run_bit_flipping_discrete_bp_program( n, m )
                if key not in execution_time_discrete_dict:
                    execution_time_discrete_dict[key] = execution_time_discrete
                    memory_usage_discrete_dict[key] = memory_usage_discrete
                else:
                    execution_time_discrete_dict[key] += execution_time_discrete
                    memory_usage_discrete_dict[key] = memory_usage_discrete

    for key in n_x_m_dict.keys():
        execution_time_discrete_dict[key] /= number_of_experiments # average the execution time
        execution_time_discrete_dict[key] = 1000 * execution_time_discrete_dict[key] # From seconds to milliseconds
        # print(f"{key} Avg. Execution time: ", execution_time_discrete_dict[key])

        memory_usage_discrete_dict[key] /= number_of_experiments  # average the execution time
        memory_usage_discrete_dict[key] = 1000 * memory_usage_discrete_dict[key]  # From seconds to milliseconds
        # print(f"{key} Avg. Memory usage: ", memory_usage_discrete_dict[key])

        row = [key, n_x_m_dict[key], execution_time_discrete_dict[key], memory_usage_discrete_dict[key], 0.0, 0.0]
        writer.writerow(row)
        print(",".join([str(x) for x in row]))

if __name__ == '__main__':
    try:
        with open(init_statistics_file(), mode="w", newline="") as csvfile:
            current_datetime = datetime.datetime.now()
            run_experiemnts(csvfile, 3, 3, 3)
    except KeyboardInterrupt:
        # this code handles keyboard interrupt
        print("Keyboard interrupt")
    except IOError as e:
        print(f"An error occurred: {e}")