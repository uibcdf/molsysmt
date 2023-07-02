import molsysmt as msm
import numpy as np
from pathlib import Path
import os
import shutil

data_dir = Path('../../data/.')

# Purge

files_to_be_purged = [
        'msmpk/lysine_dipeptide.msmpk',
        ]

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)

# Make

molsys = msm.build.build_peptide('AceLysNme')
molsys = msm.convert(molsys, to_form='lysine_dipeptide.msmpk')
shutil.move('lysine_dipeptide.msmpk', Path(data_dir, 'msmpk/lysine_dipeptide.msmpk'))


