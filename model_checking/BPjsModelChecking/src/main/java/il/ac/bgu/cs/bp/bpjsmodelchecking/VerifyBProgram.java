package il.ac.bgu.cs.bp.bpjsmodelchecking;

import il.ac.bgu.cs.bp.bpjs.analysis.*;
import il.ac.bgu.cs.bp.bpjs.analysis.listeners.PrintDfsVerifierListener;
import il.ac.bgu.cs.bp.bpjs.execution.BProgramRunner;
import il.ac.bgu.cs.bp.bpjs.execution.listeners.PrintBProgramRunnerListener;
import il.ac.bgu.cs.bp.bpjs.model.BProgram;
import il.ac.bgu.cs.bp.bpjs.model.ResourceBProgram;


public class VerifyBProgram {
    
    public static void main(String[] args) throws Exception {
        if (args.length < 1){
            //args = new String[]{"hot_cold", "30", "2", "true", "false"};
            args = new String[]{"dining_philosophers", "2", "false", "true"};
            //args = new String[]{"ttt", "2", "2", "false", "true"};
        }
        BProgram bprog = null;
        DfsBProgramVerifier vfr = null;
        if (args[0].equals("hot_cold")){
            bprog = new ResourceBProgram("hot_cold.js");
            bprog.putInGlobalScope("N", Integer.parseInt(args[1]));
            bprog.putInGlobalScope("M", Integer.parseInt(args[2]));
            bprog.putInGlobalScope("SOLVED", Boolean.parseBoolean(args[3]));
            vfr = new DfsBProgramVerifier();
            vfr.addInspection(ExecutionTraceInspections.HOT_BTHREADS);
            vfr.addInspection(ExecutionTraceInspections.HOT_SYSTEM);
            vfr.addInspection(ExecutionTraceInspections.HOT_TERMINATIONS);
            if (Boolean.parseBoolean(args[4])){
                vfr.setMaxTraceLength(Integer.parseInt(args[1] + 5));
            }
        }
        if (args[0].equals("dining_philosophers")){
            bprog = new ResourceBProgram("dining_philosophers.js");
            bprog.putInGlobalScope("PHILOSOPHER_COUNT", Integer.parseInt(args[1]));
            bprog.putInGlobalScope("SOLVED", Boolean.parseBoolean(args[2]));
            vfr = new DfsBProgramVerifier();
            vfr.addInspection(ExecutionTraceInspections.DEADLOCKS);
            if (Boolean.parseBoolean(args[3])){
                vfr.setMaxTraceLength(10);
            }
        }
        if (args[0].equals("ttt")){
            bprog = new ResourceBProgram("ttt.js");
            bprog.putInGlobalScope("R", Integer.parseInt(args[1]));
            bprog.putInGlobalScope("C", Integer.parseInt(args[2]));
            bprog.putInGlobalScope("SOLVED", Boolean.parseBoolean(args[3]));
            vfr = new DfsBProgramVerifier();
            vfr.addInspection(ExecutionTraceInspections.HOT_TERMINATIONS);
            if (Boolean.parseBoolean(args[4])){
                vfr.setMaxTraceLength((long) Integer.parseInt(args[1]) *Integer.parseInt(args[2]) + 5);
            }

        }
        //vfr.setDebugMode(true);
        //vfr.setProgressListener(new PrintDfsVerifierListener());
        VerificationResult res = vfr.verify(bprog);

        System.out.println(res.isViolationFound());  // true iff a counter example was found
        System.out.println(res.getViolation());      // an Optional<Violation>
        if (res.isViolationFound()){
            ArrayExecutionTrace trace = (ArrayExecutionTrace) res.getViolation().get().getCounterExampleTrace();
            if (trace.isCyclic()){
                System.out.println("Cyclic trace");
                int c = 0;
                for (ExecutionTrace.Entry entry : trace.getNodes()){
                    if (c == trace.getCycleToIndex()){
                        System.out.println("---------- Cycle starts here -------");
                    }
                    System.out.println(entry.getEvent());
                    c++;
                }
            } else {
                for (ExecutionTrace.Entry entry : trace.getNodes()){
                    System.out.println(entry.getEvent());
                }
            }

        }

//        BProgramRunner rnr = new BProgramRunner(bprog);
//
//        // Print program events to the console
//        rnr.addListener( new PrintBProgramRunnerListener() );
//
//        // go!
//        rnr.run();

    }
    
}
