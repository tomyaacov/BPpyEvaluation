import re
import numpy as np

# extracts the time taken and result from storm output
# add to model generation time

def q_params(min_doors=3,max_doors=10):
    combs = []
    for d in range(min_doors, max_doors+1):
        for p in range(1, d):
            for o in range(1, d-p):
                if (d >= 9) and (o>= 4): # storm stilll running...
                    pass
                elif (o < 6):
                    combs.append((d,p,o))
    return combs
combs = q_params(3, 10)

def read_time_taken(fname='modeling/time_taken.txt'):
    rgx_parse = r'time for \((\d+), (\d+), (\d+)\): ([\d.]+)'
    with open(fname) as f:
        content = f.read()
    found = re.findall(rgx_parse, content)
    entries = {}
    for entry in found:
        time = float(entry[-1])
        size = tuple([int(e) for e in entry[:3]])
        entries[size] = time
    return entries

def extract_data_storm(params):
    rgx_parse = r'Time for model input parsing: ([\d|.]+)\S.'
    rgx_cons = r'Time for model construction: ([\d|.]+)\S'
    rgx_check = r'Time for model checking: ([\d|.]+)\S.'
    rgx_res = r'Result \(for initial states\): ([\d|.]+)'
    rgx_states = r'States: 	([\d]+)'
    stats_rgx = [rgx_parse, rgx_cons, rgx_check, rgx_res, rgx_states]

    try:
        with open('modeling/res_{}d{}p{}o.txt'.format(*params)) as f:
            content = f.read()
            if len(content) == 0:
                print(f'missing file for {params}')
                return
    except:
        print(f'missing file for {params}')
        return
    found = [re.findall(phrase, content) for phrase in stats_rgx]
    if [] in found:
        print(f'missing content for {params}')
        return
    found = [f[0] for f in found]
    floats = [float(t) for t in found[0:-1]]
    states = int(found[-1])
    return floats + [states]

storm_info = {i: extract_data_storm(i) for i in combs}
const_time = read_time_taken()

# d, p, o : bp_gen_t, input_parse_t, model_cons_t, model_check_t, result, states_num
log_data = {p: [const_time[p]] + data  for p, data in storm_info.items()}

def write_overview(data):
    fname = 'gen_overview.csv'
    with open(fname, 'w+') as f:
        f.write('d, p, o, states, total_time, res\n')
        for params, entry in data.items():
            f.write(str(params)[1:-1])
            f.write(f', {entry[-1]}, {sum(entry[0:3])}, {entry[-2]}\n')
    print(f'written {len(data)} to "{fname}".')

def cum_times(data):
    for params, entry in data.items():
        cum_times = [sum(entry[0:i]) for i in range(1,5)]
        with open('modeling/times_{}d{}p{}o.csv'.format(*params), 'w+') as f:
            f.write('cum_time, res\n')
            for t in cum_times:
                f.write(f'{t}, {entry[-2]}\n')

write_overview(log_data)
cum_times(log_data)