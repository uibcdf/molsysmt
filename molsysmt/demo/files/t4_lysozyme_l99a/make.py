import molsysmt as msm
import os
import openmm as mm
from openmm import app
from openmm import unit
from sys import stdout
from mdtraj.reporters import HDF5Reporter

# purge
print('Removing old files...')
files_to_be_purged = ['181l.pdb', '181l.mmtf', 'in_pdbid_181l.msmpk']
for filename in files_to_be_purged:
    if os.path.isfile(filename):
        os.remove(filename)

# 181l pdb and mmtf files
print('Protein Data Bank files...')
msm.convert('pdbid:181l', to_form='181l.pdb')
msm.convert('pdbid:181l', to_form='181l.mmtf')

# in pdbid 181l
print('pdbid 181l in msmpk file...')
molsys = msm.convert('pdbid:181l', to_form='molsysmt.MolSys')
_ = msm.convert(molsys, to_form='in_pdbid_181l.msmpk')

