import molsysmt as msm
import pathlib import Path
import os

from fff in  Path('.').glob('*.msmpk'):
    os.remove('*.msmpk')

molsys = msm.build.build_peptide(['AceProNme',{'forcefield':'AMBER14', 'implicit_solvent':'OBC1'}])
molsys = msm.convert(molsys, to_form='proline_dipeptide_vacuum.msmpk')
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

molsys = msm.convert('1tcd.mmtf', to_form='molsysmt.MolSys')
molsys = msm.convert(molsys, to_form='TcTIM_in_pdbid_1tcd.msmpk')
del(molsys)


