import molsysmt as msm
import os
import shutil
from pathlib import Path


data_dir = Path('../.')

# purge

files_to_be_purged = [
        'h5msm/1l2y.h5msm',
        'pdb/1l2y.pdb',
        ]

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)


# 1tcd pdb, mmtf and msmpk files
print('Protein Data Bank files...')
_ = msm.convert('pdb_id:1l2y', to_form='1l2y.pdb')
shutil.move('1l2y.pdb', Path(data_dir, 'pdb/1l2y.pdb'))
_ = msm.convert('pdb_id:1l2y', to_form='1l2y.h5msm')
shutil.move('1l2y.h5msm', Path(data_dir, 'h5msm/1l2y.h5msm'))


