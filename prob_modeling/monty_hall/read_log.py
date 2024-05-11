import re
import numpy as np
from monty import param_combs

# extracts the time taken and result from storm output
# add to model generation time

def read_time_taken(fname='models/time_taken.txt'):
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

def extract_data_re(content):
    rgx_parse = r'Time for model input parsing: ([\d|.]+)\S.'
    rgx_cons = r'Time for model construction: ([\d|.]+)\S'
    rgx_check = r'Time for model checking: ([\d|.]+)\S.'
    rgx_res = r'Result \(for initial states\): ([\d|.]+)'
    rgx_states = r'States: 	([\d]+)'
    stats_rgx = [rgx_parse, rgx_cons, rgx_check, rgx_res, rgx_states]
    found = [re.findall(phrase, content) for phrase in stats_rgx]
    if [] in found:
        return
    found = [f[0] for f in found]
    floats = [float(t) for t in found[0:-1]]
    states = int(found[-1])
    return floats + [states]

def extract_data_log(params):
    try:
        with open('models/res_{}d{}p{}o.txt'.format(*params)) as f:
            content = f.read()
            if len(content) == 0:
                print(f'missing file for {params}')
                return
    except:
        print(f'missing file for {params}')
        return
    found = extract_data_re(content)
    if [] in found:
        print(f'missing content for {params}')
        return
    return found


# for models which storm finished running
def write_overview(data):
    fname = 'translation_overview.csv'
    with open(fname, 'w+') as f:
        f.write('d,p,o,states,gen_time,check_time,res\n')
        for params, entry in data.items():
            f.write(str(params)[1:-1])
            if not None in entry:
                f.write(f', {entry[-1]}, {entry[0]}, {sum(entry[1:3])}, {entry[-2]}\n')
            else:
                f.write(f', {entry[-1]}, {entry[0]}, {None}, {None}\n')
    print(f'written {len(data)} entries to "{fname}".')


def process_files(min_doors=3, max_doors=4):
    combs = param_combs(min_doors, max_doors)
    storm_info = {i: extract_data_log(i) for i in combs}
    storm_table = {k: v or [None]*5 for k, v in storm_info.items()}
    const_time = read_time_taken()

    model_time = {p: [data] + storm_table[p] for p, data in const_time.items()}
    # d, p, o : bp_gen_t, input_parse_t, model_cons_t, model_check_t, result, states_num
    write_overview(model_time)
    
if __name__ == "__main__":
    process_files(3, 4)
