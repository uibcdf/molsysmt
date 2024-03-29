import molsysmt as msm
import os
from pathlib import Path
import shutil

data_dir = Path('../.')

# Purge

files_to_be_purged = [
        'pdb/181l.pdb',
        'mmtf/181l.mmtf',
        'h5msm/181l.h5msm',
        'pdb/1l17.pdb',
        'mmtf/1l17.mmtf',
        'h5msm/1l17.h5msm',
        'h5msm/t4_lysozyme_L99A.h5msm',
        ]

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)

# 181l pdb, mmtf, h5msm files
#print('Protein Data Bank files...')
msm.convert('pdb_id:181l', to_form='181l.pdb')
msm.convert('pdb_id:181l', to_form='181l.mmtf')
msm.convert('pdb_id:181l', to_form='181l.h5msm')
shutil.move('181l.pdb', Path(data_dir, 'pdb/181l.pdb'))
shutil.move('181l.mmtf', Path(data_dir, 'mmtf/181l.mmtf'))
shutil.move('181l.h5msm', Path(data_dir, 'h5msm/181l.h5msm'))

# 1l17 pdb, mmtf, h5msm files
msm.convert('pdb_id:1l17', to_form='1l17.pdb')
msm.convert('pdb_id:1l17', to_form='1l17.mmtf')
msm.convert('pdb_id:1l17', to_form='1l17.h5msm')
shutil.move('1l17.pdb', Path(data_dir, 'pdb/1l17.pdb'))
shutil.move('1l17.mmtf', Path(data_dir, 'mmtf/1l17.mmtf'))
shutil.move('1l17.h5msm', Path(data_dir, 'h5msm/1l17.h5msm'))

# vacuum
#print('Vacuum system in h5msm file...')
molsys = msm.convert('pdb_id:181l', to_form='molsysmt.MolSys')
molsys = msm.basic.remove(molsys, selection='group_type in ["ion", "water"]')
molsys = msm.basic.remove(molsys, selection='atom_type=="H"')
molsys = msm.build.add_missing_terminal_cappings(molsys, N_terminal='ACE', C_terminal='NME')
molsys = msm.build.add_missing_hydrogens(molsys, pH=7.4)
_ = msm.convert(molsys, to_form='t4_lysozyme_L99A.h5msm')
shutil.move('t4_lysozyme_L99A.h5msm', Path(data_dir, 'h5msm/t4_lysozyme_L99A.h5msm'))

