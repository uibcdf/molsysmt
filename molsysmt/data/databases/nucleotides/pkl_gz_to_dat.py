import pickle
import gzip

with gzip.open('group_names_dna.pkl.gz', 'rb') as fff:
    group_names = pickle.load(fff)

group_names = sorted(list(group_names))
with open('group_names_dna_2.dat', 'w') as fff:
    for ii in group_names:
        fff.write(ii+ '\n')

with gzip.open('group_names_rna.pkl.gz', 'rb') as fff:
    group_names = pickle.load(fff)

group_names = sorted(list(group_names))
with open('group_names_rna_2.dat', 'w') as fff:
    for ii in group_names:
        fff.write(ii+ '\n')

