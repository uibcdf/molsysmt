import pickle
import gzip

with gzip.open('group_names_c_terminal.pkl.gz', 'rb') as fff:
    group_names = pickle.load(fff)

group_names = sorted(list(group_names))
with open('group_names_c_terminal_2.dat', 'w') as fff:
    for ii in group_names:
        fff.write(ii+ '\n')

with gzip.open('group_names_n_terminal.pkl.gz', 'rb') as fff:
    group_names = pickle.load(fff)

group_names = sorted(list(group_names))
with open('group_names_n_terminal_2.dat', 'w') as fff:
    for ii in group_names:
        fff.write(ii+ '\n')

