import molsysmt as msm
import numpy as np
from pathlib import Path
import os
import shutil

data_dir = Path('../.')

# Purge

files_to_be_purged = [
    'pdb/1tcd.pdb',
    'mmtf/1tcd.mmtf',
    'h5msm/1tcd.h5msm'
    ]

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)

# Make

msm.convert('pdb_id:1tcd', to_form='1tcd.pdb')
msm.convert('pdb_id:1tcd', to_form='1tcd.mmtf')
msm.convert('pdb_id:1tcd', to_form='1tcd.h5msm')

shutil.move('1tcd.pdb', Path(data_dir, 'pdb/1tcd.pdb'))
shutil.move('1tcd.mmtf', Path(data_dir, 'mmtf/1tcd.mmtf'))
shutil.move('1tcd.h5msm', Path(data_dir, 'h5msm/1tcd.h5msm'))

