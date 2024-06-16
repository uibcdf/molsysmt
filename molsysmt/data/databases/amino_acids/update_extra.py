import os
import glob
import json
import pickle
import gzip

### old database

pwd = '.'

pattern = os.path.join(pwd, '*.pkl.gz')
pkl_gz_files = glob.glob(pattern)
pkl_gz_files.remove('./group_names.pkl.gz')

output = {}

for file_name in pkl_gz_files:
    with gzip.open(file_name, 'rb') as fff:
        aux_output = pickle.load(fff)
        output.update(aux_output)

### extra.json

with open('extra.json', 'r') as fff:
    extra = json.load(fff)

for name in extra.keys():
    if name not in output:
        output[name]=extra[name]
    else:
        for extra_topology in extra[name]['topology']:
            is_new = True
            for topology in output[name]['topology']:
                if set(topology['atoms'])==set(extra_topology['atoms']):
                    is_new = False
                    break
            if is_new:
                output[name]['topology'].append(extra_topology)

#### End ####

split_output = {}
for name,value in output.items():
    if name[0] not in split_output:
        split_output[name[0]]={}
    split_output[name[0]][name]=value

import gzip

for file_name, aux_output in split_output.items():
    with gzip.open(file_name+'.pkl.gz', 'wb', compresslevel=9) as fff:
        pickle.dump(aux_output, fff)

