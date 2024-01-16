import molsysmt as msm
import numpy as np
from pathlib import Path
import os
import shutil

data_dir = Path('../.')

# Purge

files_to_be_purged = [
        'h5msm/valine_dipeptide.h5msm',
        ]

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)

# Make

molsys = msm.build.build_peptide('AceValNme')
molsys = msm.convert(molsys, to_form='valine_dipeptide.h5msm')
shutil.move('valine_dipeptide.h5msm', Path(data_dir, 'h5msm/valine_dipeptide.h5msm'))

