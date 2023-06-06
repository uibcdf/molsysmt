import os
from pathlib import Path

data_dir = Path('../../data/.')

files_to_be_purged = [
        'pdb/1vii.pdb',
        'mmtf/1vii.mmtf',
        'msmpk/chicken_villin_HP35.msmpk',
        'msmpk/chicken_villin_HP35_solvated.msmpk',
        'dcd/traj_chicken_villin_HP35_solvated.dcd',
        'h5/traj_chicken_villin_HP35_solvated.h5',
        ]

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)

print('DONE')
