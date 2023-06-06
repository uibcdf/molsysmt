import os
from pathlib import Path

data_dir = Path('../../data/.')

files_to_be_purged = [
        'pdb/5zmz.pdb',
        'mmtf/5zmz.mmtf',
        ]

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)

print('DONE')
