import molsysmt as msm
import os
import openmm as mm
from openmm import app
from openmm import unit
from sys import stdout
from mdtraj.reporters import HDF5Reporter


# purge
print('Removing old files...')
files_to_be_purged = ['1l2y.pdb', '1l2y.mmtf']
for filename in files_to_be_purged:
    if os.path.isfile(filename):
        os.remove(filename)

# 1tcd pdb, mmtf and msmpk files
print('Protein Data Bank files...')
msm.convert('pdb_id:1l2y', to_form='1l2y.pdb')
msm.convert('pdb_id:1l2y', to_form='1l2y.mmtf')
#msm.convert('pdb_id:1l2y', to_form='1l2y.msmpk')

