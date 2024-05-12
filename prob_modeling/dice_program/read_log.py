import re

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

def extract_data_log(n):
    try:
        with open('models/res_{}.txt'.format(n)) as f:
            content = f.read()
            if len(content) == 0:
                print(f'missing file for {n}')
                return
    except:
        print(f'missing file for {n}')
        return
    found = extract_data_re(content)
    if [] in found:
        print(f'missing content for {n}')
        return
    return found

def write_overview(data):
    fname = 'translation_overview.csv'
    with open(fname, 'w+') as f:
        f.write('n,states,gen_time,check_time,res\n')
        for params, entry in data.items():
            f.write(str(params))
            if not None in entry:
                f.write(f', {entry[-1]}, {entry[0]:.5f}, {sum(entry[1:3]):.5f}, {entry[-2]:.5f}\n')
            else:
                f.write(f', {entry[-1]}, {entry[0]:.5f}, {None}, {None}\n')
    print(f'written {len(data)} entries to "{fname}".')

def process_files(min_sides=6, max_sides=10):
    combs = range(min_sides, max_sides)
    storm_info = {i: extract_data_log(i) for i in combs}
    storm_table = {k: v or [None]*5 for k, v in storm_info.items()}
    const_time = read_time_taken()

    model_time = {p: [data] + storm_table[p] for p, data in const_time.items()}
    # n : trans_time, comp_time, result, states_num
    write_overview(model_time)
    
if __name__ == "__main__":
    process_files(6, 10)
