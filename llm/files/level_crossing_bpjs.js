
// The railway sensor system dictates the exact event order: train approaching, entering, and then leaving. Also, there is no overlapping between successive train passages.
bp.registerBThread( "railway_sensor", function(){
    while (true) {
        bp.sync( {waitFor:bp.Event("Approaching")} );
        bp.sync( {waitFor:bp.Event("Entering")} );
        bp.sync( {waitFor:bp.Event("Leaving")} );
    }
} );

// The barriers are lowered when a train is approaching and then raised as soon as possible.
bp.registerBThread( "barrier", function(){
    while (true) {
        bp.sync( {waitFor:bp.Event("Approaching")} );
        bp.sync( {request:bp.Event("Lower")} );
        bp.sync( {request:bp.Event("Raise")} );
    }
});

// A train may not enter while barriers are up.
bp.registerBThread( "train", function(){
    while (true) {
        bp.sync( {waitFor:bp.Event("Lower"), block: bp.Event("Entering")} );
        bp.sync( {waitFor:bp.Event("Raise")} );
    }
});

// The barriers may not be raised while a train is in the intersection zone. The intersection zone is the area between the approaching and leaving sensors.
