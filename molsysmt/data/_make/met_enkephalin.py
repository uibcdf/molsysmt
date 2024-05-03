import molsysmt as msm
import numpy as np
from pathlib import Path
import os
import shutil

data_dir = Path('../.')

# Purge

files_to_be_purged = [
        'h5msm/met_enkephalin.h5msm',
        'pdb/met_enkephalin.pdb',
        ]

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)

# Make

molsys = msm.build.build_peptide('TyrGlyGlyPheMet')
_ = msm.convert(molsys, to_form='met_enkephalin.h5msm')
shutil.move('met_enkephalin.h5msm', Path(data_dir, 'h5msm/met_enkephalin.h5msm'))
_ = msm.convert(molsys, to_form='met_enkephalin.pdb')
shutil.move('met_enkephalin.pdb', Path(data_dir, 'pdb/met_enkephalin.pdb'))

