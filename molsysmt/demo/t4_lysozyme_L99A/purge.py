import os
from pathlib import Path

data_dir = Path('../../data/.')

files_to_be_purged = [
        'pdb/181l.pdb',
        'mmtf/181l.mmtf',
        'msmpk/181l.msmpk',
        'pdb/1l17.pdb',
        'mmtf/1l17.mmtf',
        'msmpk/1l17.msmpk',
        'msmpk/t4_lysozyme_L99A.msmpk',
        ]

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)

print('DONE')
