from bp_modules import *
from hot_cold_scripts.hot_cold_original import *
import sys
import pynusmv
from pynusmv import prop
from pynusmv.mc import check_ltl_spec, check_explain_ltl_spec
from pynusmv.bmc.glob import bmc_setup, BmcSupport, master_be_fsm
from pynusmv.parser import parse_ltl_spec
from pynusmv.node import Node
from pynusmv.sat import SatSolverFactory, Polarity, SatSolverResult
from pynusmv.bmc import ltlspec, utils as bmcutils
import time
import tracemalloc


sys.setrecursionlimit(10000)

class ModelChecker:

    def __init__(self, event_list, bt_generators_list, bt_names_list):
        self.event_list = event_list
        self.bt_generators_list = bt_generators_list
        self.bt_names_list = bt_names_list

    def check(self, spec, bmc=True, debug=False, find_counterexample=False, bmc_length=35):
        if debug:
            print("initializing NuSMV")
            ts = time.time()
            tracemalloc.start()
        pynusmv.init.init_nusmv()
        if debug:
            print("Converting bthreads to NuSMV modules")
        bt_list = [bthread_to_module(g, n, self.event_list) for g, n in zip(self.bt_generators_list, self.bt_names_list)]
        if debug:
            print("Creating main module")
        main = main_module(self.event_list, bt_list)
        if debug:
            print("Loading model into NuSMV")

        with open("output/bp_model.smv", "w") as f:
            for bt in bt_list:
                f.write(str(bt))
                f.write("\n")
            f.write(str(main))
            f.write("\n")
            f.write("LTLSPEC " + str(spec))
        pynusmv.glob.load_from_file("output/bp_model.smv")

        if bmc:
            if debug:
                print("Computing model")
            pynusmv.glob.flatten_hierarchy()
            pynusmv.glob.encode_variables()
            pynusmv.glob.build_boolean_model()
            bmc_setup()
            spec = pynusmv.glob.prop_database()[0].expr
            if debug:
                print("Checking LTL spec")
            with BmcSupport():
                fml = Node.from_ptr(parse_ltl_spec(str(spec).strip()))
                fsm = master_be_fsm()
                problem = ltlspec.generate_ltl_problem(fsm, fml, bmc_length)
                fsm = master_be_fsm()
                cnf = problem.to_cnf(Polarity.POSITIVE)

                solver = SatSolverFactory.create()
                solver += cnf
                solver.polarity(cnf, Polarity.POSITIVE)
                solution = solver.solve()
                if debug:
                    print("Done in", time.time() - ts, "seconds")
                    print("Memory usage (bytes):", tracemalloc.get_traced_memory()[1])
                    tracemalloc.stop()
                result = solution != SatSolverResult.SATISFIABLE

                if not result and find_counterexample:
                    if debug:
                        print("Finding counterexample")
                    cnt_ex = bmcutils.generate_counter_example(fsm, problem, solver, bmc_length, "Violation")
                    explanation_str = ""
                    first_loop_siganl = False
                    for step in cnt_ex:
                        if step.is_loopback:
                            if first_loop_siganl:
                                break
                            first_loop_siganl = True
                            explanation_str += "-- Loop starts here" + "\n"
                        for symbol, value in step:
                            if str(symbol) == "event":
                                explanation_str += str(value) + "\n"
                else:
                    explanation_str = None
        else:
            if debug:
                print("Computing model")
            pynusmv.glob.compute_model()

            # spec = prop.ag(prop.af(prop.atom(("must_finish = FALSE"))))
            spec = pynusmv.glob.prop_database()[0].expr

            if debug:
                print("Checking LTL spec")
            #fsm = pynusmv.glob.prop_database().master.bddFsm
            result = check_ltl_spec(spec)
            if debug:
                print("Done in", time.time() - ts, "seconds")
                print("Memory usage (bytes):", tracemalloc.get_traced_memory()[1])
                tracemalloc.stop()
            if not result and find_counterexample:
                from pynusmv.mc import explain, eval_ctl_spec
                if debug:
                    print("Finding counterexample")
                _, explanation = check_explain_ltl_spec(spec)
                explanation_str = ""
                for state in explanation[2:-1:2]:
                    if state == explanation[2::2][-1]:
                        explanation_str += "-- Loop starts here" + "\n"
                    explanation_str += state["event"] + "\n"
                # skip_last = False
                # explanation_str = ""
                # for state in explanation[2::2]:
                #     if state == explanation[-1]:
                #         if skip_last:
                #             break
                #         skip_last = True
                #         explanation_str += "-- Loop starts here" + "\n"
                #     explanation_str += state.get_str_values()["event"] + "\n"
                # for state in explanation[::2]:
                #     if state == explanation[-1]:
                #         print("-- Loop starts here")
                #     d = {k: v for k, v in state.get_str_values().items() if
                #          k in ["event", "bt0.state", "bt1.state", "bt2.state", "bt0.must_finish", "bt1.must_finish",
                #                "bt2.must_finish", "must_finish"]}
                #     print(d)
            else:
                explanation_str = None

        pynusmv.init.deinit_nusmv()
        return result, explanation_str


