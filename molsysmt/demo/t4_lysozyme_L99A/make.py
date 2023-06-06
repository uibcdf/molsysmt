import molsysmt as msm
import os
from pathlib import Path
import shutil

data_dir = Path('../../data/.')

# 181l pdb, mmtf, msmpk files
print('Protein Data Bank files...')
msm.convert('pdb_id:181l', to_form='181l.pdb')
msm.convert('pdb_id:181l', to_form='181l.mmtf')
msm.convert('pdb_id:181l', to_form='181l.msmpk')
shutil.move('181l.pdb', Path(data_dir, 'pdb/181l.pdb'))
shutil.move('181l.mmtf', Path(data_dir, 'mmtf/181l.mmtf'))
shutil.move('181l.msmpk', Path(data_dir, 'msmpk/181l.msmpk'))

# 1l17 pdb, mmtf, msmpk files
msm.convert('pdb_id:1l17', to_form='1l17.pdb')
msm.convert('pdb_id:1l17', to_form='1l17.mmtf')
msm.convert('pdb_id:1l17', to_form='1l17.msmpk')
shutil.move('1l17.pdb', Path(data_dir, 'pdb/1l17.pdb'))
shutil.move('1l17.mmtf', Path(data_dir, 'mmtf/1l17.mmtf'))
shutil.move('1l17.msmpk', Path(data_dir, 'msmpk/1l17.msmpk'))

# vacuum
print('Vacuum system in msmpk file...')
molsys = msm.convert('pdb_id:181l', to_form='molsysmt.MolSys')
molsys = msm.basic.remove(molsys, selection='group_type in ["ion", "water"]')
molsys = msm.basic.remove(molsys, selection='atom_type=="H"')
molsys = msm.build.add_missing_terminal_cappings(molsys, N_terminal='ACE', C_terminal='NME')
molsys = msm.build.add_missing_hydrogens(molsys, pH=7.4)
_ = msm.convert(molsys, to_form='t4_lysozyme_L99A.msmpk')
shutil.move('t4_lysozyme_L99A.msmpk', Path(data_dir, 'msmpk/t4_lysozyme_L99A.msmpk'))

