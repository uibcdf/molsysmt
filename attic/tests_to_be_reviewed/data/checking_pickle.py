import pickle

with open('1tcd.pickle', 'rb') as f:
    expected_values = pickle.load(f)

print(expected_values['step_from_system_1'])
print(expected_values['time_from_system_1'])

