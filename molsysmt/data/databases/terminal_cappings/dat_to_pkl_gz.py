import pickle
import gzip

group_names = []
with open('group_names_c_terminal.dat', 'r') as fff:
    for line in fff:
        group_names.append(line.strip())

with gzip.open('group_names_c_terminal.pkl.gz', 'wb', compresslevel=9) as fff:
    pickle.dump(set(group_names), fff)

group_names = []
with open('group_names_n_terminal.dat', 'r') as fff:
    for line in fff:
        group_names.append(line.strip())

with gzip.open('group_names_n_terminal.pkl.gz', 'wb', compresslevel=9) as fff:
    pickle.dump(set(group_names), fff)

