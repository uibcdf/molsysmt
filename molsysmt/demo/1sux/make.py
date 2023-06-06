import molsysmt as msm
import os
import shutil
from pathlib import Path

data_dir = Path('../../data')

msm.convert('pdb_id:1vii', to_form='1vii.pdb')
shutil.move('1vii.pdb', Path(data_dir, 'pdb/1vii.pdb'))

msm.convert('pdb_id:1vii', to_form='1vii.mmtf')
shutil.move('1vii.mmtf', Path(data_dir, 'mmtf/1vii.mmtf'))

print('DONE')

