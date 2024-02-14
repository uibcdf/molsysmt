import molsysmt as msm
import os
import shutil
from pathlib import Path

data_dir = Path('../../../data')

# Purge

files_to_be_purged = [
        'pdb/5zmz.pdb',
        'mmtf/5zmz.mmtf',
        ]

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)

# Make

msm.convert('pdb_id:5zmz', to_form='5zmz.pdb')
shutil.move('5zmz.pdb', Path(data_dir, 'pdb/5zmz.pdb'))

msm.convert('pdb_id:5zmz', to_form='5zmz.mmtf')
shutil.move('5zmz.mmtf', Path(data_dir, 'mmtf/5zmz.mmtf'))

print('DONE')

