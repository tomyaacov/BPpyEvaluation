// if (!PHILOSOPHER_COUNT)  PHILOSOPHER_COUNT = 2
// if (!SOLVED) SOLVED = false;

// const PHILOSOPHER_COUNT = 2;
// const SOLVED = false;

const Take = (i, side) => bp.Event('T' + i.toString() + side.toString())
const Put = (i, side) => bp.Event('P' + i.toString() + side.toString())
const AnyTake = i => [Take(i, "R"), Take((i + 1) % PHILOSOPHER_COUNT, "L")]
const AnyPut = i => [Put(i, "R"), Put((i + 1) % PHILOSOPHER_COUNT, "L")]

for (let c = 0; c < PHILOSOPHER_COUNT; c++) {
    let i = c
    bp.registerBThread('Fork ' + i + ' behavior', function () {
        while (true) {
            if (bp.sync({waitFor: AnyTake(i), block: AnyPut(i)}).name.endsWith("R")) {
                bp.sync({waitFor: AnyPut(i), block: AnyTake(i).concat([Put((i + 1) % PHILOSOPHER_COUNT, "L")])})
            } else {
                bp.sync({waitFor: AnyPut(i), block: AnyTake(i).concat([Put(i, "R")])})

            }
        }
    })

    bp.registerBThread('Philosopher ' + i + ' behavior', function () {
        while (true) {
            bp.sync({request: [Take(i, 'R'), Take(i, 'L')]})
            bp.sync({request: [Take(i, 'R'), Take(i, 'L')]})
            bp.sync({request: [Put(i, 'R'), Put(i, 'L')]})
            bp.sync({request: [Put(i, 'R'), Put(i, 'L')]})
        }
    })

}

bp.registerBThread('fork' + 0 + "eventually_released", function () {
    while (true) {
        bp.sync({waitFor: AnyTake(0)})
        bp.hot(true).sync({waitFor: AnyPut(0)})
    }
})

if (SOLVED){
    const TakeSemaphore = i => bp.Event('TS' + i.toString())
    const ReleaseSemaphore = i => bp.Event('RS' + i.toString())
    const AnyTakeSemaphore = bp.EventSet('AnyTakeSemaphore', function (e) {
        return e.name.startsWith('TS')
    })
    const AnyReleaseSemaphore = bp.EventSet('AnyReleaseSemaphore', function (e) {
        return e.name.startsWith('RS')
    })

    bp.registerBThread('Semaphore', function () {
        while (true) {
            bp.sync({waitFor: AnyTakeSemaphore})
            bp.sync({waitFor: AnyReleaseSemaphore, block: AnyTakeSemaphore})
        }
    })
    for (let c = 0; c < PHILOSOPHER_COUNT; c++) {
        let i = c
        bp.registerBThread('Take semaphore ' + i, function () {
            while (true) {
                bp.sync({request: TakeSemaphore(i), block: [Take(i, 'R'), Take(i, 'L')]})
                bp.sync({waitFor: [Take(i, 'R'), Take(i, 'L')]})
                bp.sync({waitFor: [Take(i, 'R'), Take(i, 'L')]})
                bp.sync({request: ReleaseSemaphore(i), block: [Put(i, 'R'), Put(i, 'L')]})
                bp.sync({waitFor: [Put(i, 'R'), Put(i, 'L')]})
                bp.sync({waitFor: [Put(i, 'R'), Put(i, 'L')]})
            }
        })
    }
}



// // ############  Liveness requirements  ##############
// for (let c = 1; c <= PHILOSOPHER_COUNT; c++) {
//     let i = c
//
//     // A taken fork will eventually be released
//     bthread('[](take -> <>put)', function () {
//         while (true) {
//             sync({waitFor: AnyTake(i)})
//             hot(true).sync({waitFor: AnyPut(i)})
//         }
//     })
//
//     // A hungry philosopher will eventually eat
//     bthread('NoStarvation', function () {
//         while (true) {
//             hot(true).sync({waitFor: Take(i, 'L')})
//             sync({waitFor: Put(i, 'R')})
//         }
//     })
// }
//
//
// // ############  SOLUTION 1 - Semaphore  ##############
// const TakeSemaphore = i => bp.Event('TakeSemaphore', i)
// const ReleaseSemaphore = i => bp.Event('ReleaseSemaphore', i)
// const AnyTakeSemaphore = bp.EventSet('AnyTakeSemaphore', function (e) {
//     return e.name == 'TakeSemaphore'
// })
// const AnyReleaseSemaphore = bp.EventSet('AnyReleaseSemaphore', function (e) {
//     return e.name == 'ReleaseSemaphore'
// })

/*bthread('Semaphore', function () {
  while (true) {
    sync({waitFor: AnyTakeSemaphore})
    sync({waitFor: AnyReleaseSemaphore, block: AnyTakeSemaphore})
  }
})
for (let c = 1; c <= PHILOSOPHER_COUNT; c++) {
  let i = c
  bthread('Take semaphore ' + i, function () {
    while (true) {
      sync({request: TakeSemaphore(i), block: [Take(i, 'R'), Take(i, 'L')]})
      sync({waitFor: [Take(i, 'R'), Take(i, 'L')]})
      sync({waitFor: [Take(i, 'R'), Take(i, 'L')]})
      sync({request: ReleaseSemaphore(i), block: [Put(i, 'R'), Put(i, 'L')]})
      sync({waitFor: [Put(i, 'R'), Put(i, 'L')]})
      sync({waitFor: [Put(i, 'R'), Put(i, 'L')]})
    }
  })
}*/

// bp.registerBThread('mark state as accepting', function () {
//     while (true) {
//         if (use_accepting_states) {
//             AcceptingState.Continuing()
//             // AcceptingState.Stopping()
//         }
//         bp.sync({ waitFor: bp.all })
//     }
// })