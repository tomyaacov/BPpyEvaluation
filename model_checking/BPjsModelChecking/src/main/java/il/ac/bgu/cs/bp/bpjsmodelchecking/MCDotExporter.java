package il.ac.bgu.cs.bp.bpjsmodelchecking;

import il.ac.bgu.cs.bp.statespacemapper.MapperResult;
import il.ac.bgu.cs.bp.statespacemapper.jgrapht.MapperEdge;
import il.ac.bgu.cs.bp.statespacemapper.jgrapht.MapperVertex;
import il.ac.bgu.cs.bp.statespacemapper.jgrapht.exports.DotExporter;
import org.jgrapht.nio.Attribute;
import org.jgrapht.nio.DefaultAttribute;

import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;
import java.util.function.Supplier;

public class MCDotExporter  extends DotExporter {

    private Function<String, String> sanitizerProvider;

    public MCDotExporter(MapperResult res, String path, String runName) {
        super(res, path, runName);
        this.sanitizerProvider = sanitizerProvider();
    }

    protected Function<MapperEdge, Map<String, Attribute>> edgeAttributeProvider() {
        return e -> new HashMap<>(Map.of(
                "label", DefaultAttribute.createAttribute(sanitizerProvider.apply(e.event.getName()))
        ));
    }

    @Override
    protected Supplier<Map<String, Attribute>> graphAttributeProvider() {
        return HashMap::new;
    }
}
