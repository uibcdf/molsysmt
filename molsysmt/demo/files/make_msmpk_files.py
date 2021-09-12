import molsysmt as msm
import numpy as np
from pathlib import Path
import os

# Removing all msmpk files

for msmpk_file in Path('.').glob('*.msmpk'):
    os.remove(msmpk_file)

# New msmpk files

molsys = msm.build.build_peptide(['AceAlaNme',{'forcefield':'AMBER14', 'implicit_solvent':'OBC1'}])
molsys = msm.convert(molsys, to_form='alanine_dipeptide_vacuum.msmpk')
del(molsys)

molsys = msm.build.build_peptide(['AceValNme',{'forcefield':'AMBER14', 'implicit_solvent':'OBC1'}])
molsys = msm.structure.translate(molsys, translation='[-1.0, 0.0, 0.0] nanometers')
molsys = msm.convert(molsys, to_form='valine_dipeptide_vacuum.msmpk')
del(molsys)

molsys = msm.build.build_peptide(['AceLysNme',{'forcefield':'AMBER14', 'implicit_solvent':'OBC1'}])
molsys = msm.structure.translate(molsys, translation='[1.0, 0.0, 0.0] nanometers')
molsys = msm.convert(molsys, to_form='lysine_dipeptide_vacuum.msmpk')
del(molsys)

molsys = msm.convert('pdbid:181L', to_form='molsysmt.MolSys')
molsys = msm.convert(molsys, to_form='T4_Lysozyme_L99A_in_pdbid_181l.msmpk')
del(molsys)

molsys = msm.convert('pdbid:1vii', to_form='molsysmt.MolSys')
molsys = msm.convert(molsys, to_form='Villin_HP35_in_pdbid_1vii.msmpk')
del(molsys)

molsys = msm.convert('pdbid:1brs', to_form='molsysmt.MolSys')
molsys = msm.convert(molsys, to_form='Barnase_Barstar_in_pdbid_1brs.msmpk')
del(molsys)

molsys = msm.convert('pdbid:4m6j', to_form='molsysmt.MolSys')
molsys = msm.convert(molsys, to_form='DHFR_in_pdbid_4m6j.msmpk')
del(molsys)

molsys = msm.convert('pdbid:4m6j', to_form='molsysmt.MolSys')
molsys = msm.convert(molsys, to_form='DHFR_in_pdbid_4m6j.msmpk')
del(molsys)


