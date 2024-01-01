import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import *
from bppy.analysis.bprogram_converter import BProgramConverter
from bppy.utils.dfs import DFSBProgram
import itertools
import time


@bp.thread
def game_show(doors_num, prizes_num, doors_opened_num):
    prizes = []
    doors = [x for x in range(doors_num)]
    for i in range(prizes_num):
        doors_possible = [d for d in doors if d not in prizes]
        hide = yield choice({i: 1 / len(doors_possible) for i in doors_possible})#doors_possible[0]#yield choice({i: 1 / len(doors_possible) for i in doors_possible})
        prizes.append(hide)
        prizes = sorted(prizes)
    for hide in prizes:
        yield sync(request=bp.BEvent(f'hide{hide}'))
        #print(f'hide{hide}')
    yield sync(request=bp.BEvent('done_hiding'))
    #print('done hiding')
    guess = yield sync(waitFor=[bp.BEvent(f'guess{i}') for i in doors])
    #print(f'guess{guess}')
    doors_opened = []
    cant_be_opened = prizes + [int(guess.name.replace('guess', ''))]
    for o in range(doors_opened_num):
        possible_opens = [d for d in doors if d not in cant_be_opened]
        opened = yield choice({door: 1 / len(possible_opens) for door in possible_opens})#possible_opens[0]#yield choice({door: 1 / len(possible_opens) for door in possible_opens})
        doors_opened.append(opened)
        doors_opened = sorted(doors_opened)
        cant_be_opened.append(opened)
        cant_be_opened = sorted(cant_be_opened)
    for opened in doors_opened:
        yield sync(request=bp.BEvent(f'open{opened}'))
        #print(f'open{opened}')


@bp.thread
def contestant(doors_num):
    doors = [x for x in range(doors_num)]
    yield sync(waitFor=bp.BEvent('done_hiding'))
    guess = yield choice({i: 1 / len(doors) for i in doors})#doors[0]#yield choice({i: 1 / len(doors) for i in doors})
    yield sync(request=bp.BEvent(f'guess{guess}'))


options = [
    [5, 1, 1],
    [5, 3, 1],
    [5, 1, 3],
    [10, 1, 1],
    [10, 5, 1],
    [10, 1, 5],
    [10, 3, 3],
    [15, 1, 1],
    [15, 7, 1],
    [15, 1, 7],
    [15, 5, 5],
    [20, 1, 1],
    [20, 10, 1],
    [20, 1, 10],
    [20, 7, 7],

]


for option in options:
    DOORS_NUM, PRIZES_NUM, DOORS_OPENED_NUM = option


    bp_gen = lambda: bp.BProgram(bthreads=[game_show(DOORS_NUM, PRIZES_NUM, DOORS_OPENED_NUM), contestant(DOORS_NUM)],
                                 event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                                 listener=bp.PrintBProgramRunnerListener())

    # bp_gen().run()
    #
    # raise ValueError('stop')


    dfs = DFSBProgram(bp_gen,
                      [bp.BEvent(f'hide{hide}') for hide in range(DOORS_NUM)] + [bp.BEvent('done_hiding')] +
                      [bp.BEvent(f'guess{guess}') for guess in range(DOORS_NUM)] +
                      [bp.BEvent(f'open{open}') for open in range(DOORS_NUM)],
                      max_trace_length=10**10)
    start = time.time()
    init, mapper = dfs.run(explore_graph=False)
    end = time.time()
    print("------------------------------------")
    print("DOORS_NUM:", DOORS_NUM, "PRIZES_NUM:", PRIZES_NUM, "DOORS_OPENED_NUM:", DOORS_OPENED_NUM)
    print("TIME:", end - start)
    print("STATES:")
    for i in mapper:
        print(i, len(mapper[i]))