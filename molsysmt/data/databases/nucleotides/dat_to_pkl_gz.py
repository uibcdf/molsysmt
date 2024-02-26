import pickle
import gzip

group_names = []
with open('group_names_dna.dat', 'r') as fff:
    for line in fff:
        group_names.append(line.strip())

with gzip.open('group_names_dna.pkl.gz', 'wb', compresslevel=9) as fff:
    pickle.dump(group_names, fff)

group_names = []
with open('group_names_rna.dat', 'r') as fff:
    for line in fff:
        group_names.append(line.strip())

with gzip.open('group_names_rna.pkl.gz', 'wb', compresslevel=9) as fff:
    pickle.dump(group_names, fff)

