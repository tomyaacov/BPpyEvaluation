import datetime
import csv
import logging
from cinderella_discrete import run_cinderella_discrete_bp_program
from cinderella_smt import run_cinderella_smt_bp_program

def init_statistics_file():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"statistics_{timestamp}.csv"
    return filename


def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--n", type=int, default=5, help="Number of buckets"
    )
    parser.add_argument(
        "-c", "--c", type=int, default=2, help="Number of adjacent buckets Cinderella empties"
    )
    parser.add_argument(
        "-b", "--b", type=int, default=9, help="Maximum number of water units a bucket can contain"
    )
    parser.add_argument(
        "-a", "--a", type=int, default=5, help="Number of water units the stepmother pours into the buckets"
    )
    parser.add_argument(
        "-n_e", "--num_of_exp", type=int, default=3, help="The number of times to run the experiment"
    )
    args = parser.parse_args()
    return args.n, args.c, args.b, args.a, args.num_of_exp

def run_experiemnts(csvfile, n, c, b,  a, number_of_experiments=1):


    header = [
        "N",
        "C",
        "B",
        "A",
        "execution_time_discrete",
        "memory_usage_discrete",
        "execution_time_smt",
        "memory_usage_smt",
    ]

    writer = csv.writer(csvfile, delimiter=",")
    writer.writerow(header)
    logging.info(",".join(header))

    execution_time_discrete_dict = {}
    memory_usage_discrete_dict = {}
    execution_time_smt_dict = {}
    memory_usage_smt_dict = {}

    logging.info("Starting Cinderella experiments...")
    for exp in range(number_of_experiments):
        for current_b in range(1, b+1):
            execution_time_discrete,memory_usage_discrete = run_cinderella_discrete_bp_program( n, c, current_b,  a )
            execution_time_smt, memory_usage_smt = run_cinderella_smt_bp_program(n, c, current_b, a)
            if current_b not in execution_time_discrete_dict:
                execution_time_discrete_dict[current_b] = execution_time_discrete
                memory_usage_discrete_dict[current_b] = memory_usage_discrete
                execution_time_smt_dict[current_b] = execution_time_smt
                memory_usage_smt_dict[current_b] = memory_usage_smt
            else:
                execution_time_discrete_dict[current_b] += execution_time_discrete
                memory_usage_discrete_dict[current_b] += memory_usage_discrete
                execution_time_smt_dict[current_b] += execution_time_smt
                memory_usage_smt_dict[current_b] += memory_usage_smt
            logging.info(f"Finished Cinderella execution for b: {current_b}")
        logging.info(f"Finished experiment {exp+1} out of {number_of_experiments}")
        logging.info("---------------------------------------------------")
    logging.info("Finished Cinderella experiments...")

    logging.info("Starting Cinderella results processing...")
    for current_b in range(1, b+1):
        execution_time_discrete_dict[current_b] /= number_of_experiments # average the execution time
        execution_time_discrete_dict[current_b] = 1000 * execution_time_discrete_dict[current_b] # From seconds to milliseconds
        # logging.info(f"{key} Avg. Execution time discrete: ", execution_time_discrete_dict[key])

        memory_usage_discrete_dict[current_b] /= number_of_experiments  # average the memory usage,units in KB
        # logging.info(f"{key} Avg. Memory usage discrete: ", memory_usage_discrete_dict[key])

        execution_time_smt_dict[current_b] /= number_of_experiments # average the execution time
        execution_time_smt_dict[current_b] = 1000 * execution_time_smt_dict[current_b] # From seconds to milliseconds
        # logging.info(f"{key} Avg. Execution time smt: ", execution_time_smt_dict[key])

        memory_usage_smt_dict[current_b] /= number_of_experiments  # average the memory usage, units in KB
        # logging.info(f"{key} Avg. Memory usage: smt", memory_usage_smt_dict[key])

        row = [n, c, current_b, a, execution_time_discrete_dict[current_b], memory_usage_discrete_dict[current_b], execution_time_smt_dict[current_b], memory_usage_smt_dict[current_b]]
        writer.writerow(row)
        logging.info(",".join([str(x) for x in row]))
    logging.info("Finished Cinderella results processing...")

if __name__ == '__main__':
    try:
        with open(init_statistics_file(), mode="w", newline="") as csvfile:
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            logging.basicConfig(filename=f"cinderella_experiments_{current_datetime}.log", level=logging.INFO)
            n, c, b,  a, num_of_exp = parse_arguments()
            logging.info(f"Starting Cinderella experiments with n: {n}, c: {c}, b: {b}, a: {a}, num_of_exp: {num_of_exp}")
            run_experiemnts(csvfile, n, c, b,  a, num_of_exp)
    except KeyboardInterrupt:
        # this code handles keyboard interrupt
        logging.info("Keyboard interrupt")
    except IOError as e:
        logging.error(f"An error occurred: {e}")