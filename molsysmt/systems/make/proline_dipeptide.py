import molsysmt as msm
import numpy as np
from pathlib import Path
import os
import shutil

data_dir = Path('../../data/.')

# Purge

files_to_be_purged = [
        'msmpk/proline_dipeptide.msmpk',
        ]

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)

# Make

molsys = msm.build.build_peptide('AceProNme')
molsys = msm.convert(molsys, to_form='proline_dipeptide.msmpk')
shutil.move('proline_dipeptide.msmpk', Path(data_dir, 'msmpk/proline_dipeptide.msmpk'))


