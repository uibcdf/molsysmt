import molsysmt as msm
import numpy as np
from pathlib import Path
import os
import shutil

data_dir = Path('../../data/.')

# Purge

files_to_be_purged = [
        'msmpk/valine_dipeptide.msmpk',
        ]

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)

# Make

molsys = msm.build.build_peptide('AceValNme')
molsys = msm.convert(molsys, to_form='valine_dipeptide.msmpk')
shutil.move('valine_dipeptide.msmpk', Path(data_dir, 'msmpk/valine_dipeptide.msmpk'))


