import pickle

with open('data/1tcd.pickle', 'rb') as f:
    expected_values = pickle.load(f)

print(expected_values['chain_index_from_chain_1'])
print(expected_values['n_chains_from_chain_1'])

