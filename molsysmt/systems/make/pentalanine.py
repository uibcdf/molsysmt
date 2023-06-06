import molsysmt as msm
import os
from mdtraj.reporters import HDF5Reporter
from pathlib import Path
import shutil

data_dir = Path('../../../data/.')

# Purge

files_to_be_purged = [
        'inpcrd/pentalanine.inpcrd',
        'prmtop/pentalanine.prmtop',
        'h5/traj_pentalanine.h5',
        ]

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)


