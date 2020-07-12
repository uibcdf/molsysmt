import pickle

with open('data/1tcd.pickle', 'rb') as f:
    expected_values = pickle.load(f)

print(expected_values['chain_id_from_atom_2'])

