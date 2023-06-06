import molsysmt as msm
import os
import shutil
from pathlib import Path

data_dir = Path('../../../data')

# Purge

files_to_be_purged = [
        'pdb/1sux.pdb',
        'mmtf/1sux.mmtf',
        ]

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)

# Make

msm.convert('pdb_id:1sux', to_form='1sux.pdb')
shutil.move('1sux.pdb', Path(data_dir, 'pdb/1sux.pdb'))

msm.convert('pdb_id:1sux', to_form='1sux.mmtf')
shutil.move('1sux.mmtf', Path(data_dir, 'mmtf/1sux.mmtf'))

print('DONE')

