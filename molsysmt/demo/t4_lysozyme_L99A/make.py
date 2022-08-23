import molsysmt as msm
import os
import openmm as mm
from openmm import app
from openmm import unit
from sys import stdout
from mdtraj.reporters import HDF5Reporter

# purge
print('Removing old files...')
files_to_be_purged = ['181l.pdb', '181l.mmtf', '1l17.pdb', '1l17.mmtf']
for filename in files_to_be_purged:
    if os.path.isfile(filename):
        os.remove(filename)

# 181l pdb, mmtf, msmpk files
print('Protein Data Bank files...')
msm.convert('pdb_id:181l', to_form='181l.pdb')
msm.convert('pdb_id:181l', to_form='181l.mmtf')
msm.convert('pdb_id:181l', to_form='181l.msmpk')

# 1l17 pdb, mmtf, msmpk files
print('Protein Data Bank files...')
msm.convert('pdb_id:1l17', to_form='1l17.pdb')
msm.convert('pdb_id:1l17', to_form='1l17.mmtf')
msm.convert('pdb_id:1l17', to_form='1l17.msmpk')

# vacuum
print('Vacuum system in msmpk file...')
molsys = msm.convert('pdb_id:181l', to_form='molsysmt.MolSys')
molsys = msm.basic.remove(molsys, selection='group_type in ["ion", "water"]')
molsys = msm.basic.remove(molsys, selection='atom_type=="H"')
molsys = msm.build.add_missing_terminal_cappings(molsys, N_terminal='ACE', C_terminal='NME')
molsys = msm.build.add_missing_hydrogens(molsys, pH=7.4)
_ = msm.convert(molsys, to_form='vacuum.msmpk')

