import molsysmt as msm
import os
import shutil
from pathlib import Path
import numpy as np

data_dir = Path('../.')

# purge
print('Removing old files...')

files_to_be_purged = [
    'bcif_gz/2nzt.bcif.gz',
    'h5msm/2nzt.h5msm']

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)

# make
print('Making new files...')
_ = msm.convert('2NZT', '2nzt.bcif.gz')
_ = msm.convert('2nzt.bcif.gz', '2nzt.h5msm')
shutil.move('2nzt.bcif.gz', Path(data_dir, 'bcif_gz/2nzt.bcif.gz'))
shutil.move('2nzt.h5msm', Path(data_dir, 'h5msm/2nzt.h5msm'))

