import molsysmt as msm
import numpy as np
from pathlib import Path
import os
import shutil

data_dir = Path('../.')

# Purge

files_to_be_purged = [
        'msmpk/popc_membrane.msmpk',
        ]

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)

# Make

psf = msm.systems['POPC membrane']['popc_membrane.psf']
dcd = msm.systems['POPC membrane']['popc_membrane.dcd']
molsys = msm.convert([psf, dcd])
molsys = msm.convert(molsys, to_form='popc_membrane.msmpk')
shutil.move('popc_membrane.msmpk', Path(data_dir, 'msmpk/popc_membrane.msmpk'))

