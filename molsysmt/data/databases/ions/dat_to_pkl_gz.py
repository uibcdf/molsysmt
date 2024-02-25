import pickle
import gzip

group_names = []
with open('group_names.dat', 'r') as fff:
    for line in fff:
        group_names.append(line.strip())

with gzip.open('group_names.pkl.gz', 'wb', compresslevel=9) as fff:
    pickle.dump(set(group_names), fff)

