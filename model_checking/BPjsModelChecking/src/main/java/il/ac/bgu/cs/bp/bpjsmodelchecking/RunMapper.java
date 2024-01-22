package il.ac.bgu.cs.bp.bpjsmodelchecking;

import il.ac.bgu.cs.bp.bpjs.analysis.DfsBProgramVerifier;
import il.ac.bgu.cs.bp.bpjs.analysis.ExecutionTraceInspections;
import il.ac.bgu.cs.bp.bpjs.model.BProgram;
import il.ac.bgu.cs.bp.bpjs.model.ResourceBProgram;
import il.ac.bgu.cs.bp.statespacemapper.MapperResult;
import il.ac.bgu.cs.bp.statespacemapper.StateSpaceMapper;
import il.ac.bgu.cs.bp.statespacemapper.jgrapht.exports.DotExporter;

import java.nio.file.Paths;

public class RunMapper {
    public static void main(String[] args) throws Exception {
        if (args.length < 1){
            //args = new String[]{"hot_cold", "3", "1", "true"};
            args = new String[]{"dining_philosophers", "1", "true"};
            //args = new String[]{"ttt", "2", "2", "false"};
        }
        BProgram bprog = null;
        if (args[0].equals("hot_cold")){
            bprog = new ResourceBProgram("hot_cold.js");
            bprog.putInGlobalScope("N", Integer.parseInt(args[1]));
            bprog.putInGlobalScope("M", Integer.parseInt(args[2]));
            bprog.putInGlobalScope("SOLVED", Boolean.parseBoolean(args[3]));
        }
        if (args[0].equals("dining_philosophers")){
            bprog = new ResourceBProgram("dining_philosophers.js");
            bprog.putInGlobalScope("PHILOSOPHER_COUNT", Integer.parseInt(args[1]));
            bprog.putInGlobalScope("SOLVED", Boolean.parseBoolean(args[2]));
        }
        if (args[0].equals("ttt")){
            bprog = new ResourceBProgram("ttt.js");
            bprog.putInGlobalScope("R", Integer.parseInt(args[1]));
            bprog.putInGlobalScope("C", Integer.parseInt(args[2]));
            bprog.putInGlobalScope("SOLVED", Boolean.parseBoolean(args[3]));
        }
        StateSpaceMapper stateSpaceMapper = new StateSpaceMapper();
        long start = System.currentTimeMillis();
        MapperResult mapperResult = stateSpaceMapper.mapSpace(bprog);
        long end = System.currentTimeMillis();
        long elapsedTime = end - start;
        System.out.println("elapsedTime:");
        System.out.println(elapsedTime);
        System.out.println(mapperResult);
        System.out.println("// Export to GraphViz...");
        String path = Paths.get("output",  "output").toString();
        DotExporter dotExporter = new MCDotExporter(mapperResult, path, "output");
        dotExporter.export();
    }
}
