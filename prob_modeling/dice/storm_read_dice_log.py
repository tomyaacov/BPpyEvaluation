import re
import numpy as np

# extracts the time taken and result from storm output
# add to model generation time


def read_time_taken(fname='models/time_taken.txt'):
    rgx_parse = r'time for (\d+): ([\d.]+)'
    with open(fname) as f:
        content = f.read()
    found = re.findall(rgx_parse, content)
    entries = {}
    for entry in found:
        time = float(entry[-1])
        size = int(entry[0])
        entries[size] = time
    return entries

def extract_data_storm(n):
    rgx_parse = r'Time for model input parsing: ([\d|.]+)\S.'
    rgx_cons = r'Time for model construction: ([\d|.]+)\S'
    rgx_check = r'Time for model checking: ([\d|.]+)\S.'
    rgx_res = r'Result \(for initial states\): ([\d|.]+)'
    rgx_states = r'States: 	([\d]+)'
    stats_rgx = [rgx_parse, rgx_cons, rgx_check, rgx_res, rgx_states]

    try:
        with open('models/res_{}.txt'.format(n)) as f:
            content = f.read()
            if len(content) == 0:
                print(f'missing file for {n}')
                return
    except:
        print(f'missing file for {n}')
        return
    found = [re.findall(phrase, content) for phrase in stats_rgx]
    if [] in found:
        print(f'missing content for {params}')
        return
    found = [f[0] for f in found]
    floats = [float(t) for t in found[0:-1]]
    states = int(found[-1])
    return floats + [states]

storm_info = {i: extract_data_storm(i) for i in range(6, 31)}
const_time = read_time_taken()

# d, p, o : bp_gen_t, input_parse_t, model_cons_t, model_check_t, result, states_num
log_data = {p: [const_time[p]] + data  for p, data in storm_info.items() if data != None}

def write_time_data():
    fname = 'gen_check_times.csv'
    with open(fname, 'w+') as f:
        f.write('n,gen_time,check_time\n')
        for p, gen_time in const_time.items():
            f.write(str(p))
            if p in storm_info and storm_info[p] != None:
                print(p, storm_info[p])
                f.write(f',{round(gen_time, 10)},{round(sum(storm_info[p][0:3]), 10)}\n')
            else:
                f.write(f',{round(gen_time, 10)},NaN\n')
    print(f'written {len(const_time)} to "{fname}".')

def write_overview(data):
    fname = 'storm_run_overview.csv'
    with open(fname, 'w+') as f:
        f.write('n, states, gen_time, check_time, res\n')
        for params, entry in data.items():
            f.write(str(params))
            f.write(f', {entry[-1]}, {entry[0]}, {sum(entry[1:4])}, {entry[-2]}\n')
    print(f'written {len(data)} to "{fname}".')

def cum_times(data):
    for n, entry in data.items():
        cum_times = [entry[0],  sum(entry[:4])]
        with open('models/times_{}.csv'.format(n), 'w+') as f:
            f.write('cum_time, res\n')
            for t in cum_times:
                f.write(f'{t}, {entry[-2]}\n')

write_time_data()
write_overview(log_data)
cum_times(log_data)