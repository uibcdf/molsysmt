import molsysmt as msm
import os
import shutil
from pathlib import Path

data_dir = Path('../../data')

msm.convert('pdb_id:5zmz', to_form='5zmz.pdb')
shutil.move('5zmz.pdb', Path(data_dir, 'pdb/5zmz.pdb'))

msm.convert('pdb_id:5zmz', to_form='5zmz.mmtf')
shutil.move('5zmz.mmtf', Path(data_dir, 'mmtf/5zmz.mmtf'))

print('DONE')

