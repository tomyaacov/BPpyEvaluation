
// When the system loads, do 'HOT' three times.
bp.registerBThread( "add_hot", function(){
    for (let i = 0; i < 3; i++) {
        bp.sync( {request:bp.Event("HOT")} );
    }
} );

// When the system loads, do 'COLD' three times.
bp.registerBThread("add_cold", function(){
    for (let i = 0; i < 3; i++) {
        bp.sync( {request:bp.Event("COLD")} );
    }
} );

// Prevent 'HOT' from being executed consecutively.
bp.registerBThread( "prevent_consecutive_hot", function(){
    while (true){
        bp.sync( {waitFor:bp.Event("HOT")} );
        bp.sync( {waitFor:bp.all, block: bp.Event("HOT")} );
    }
} );