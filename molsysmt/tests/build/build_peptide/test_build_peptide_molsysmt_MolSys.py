"""
Unit and regression test for the build peptide of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import os

# Distance between atoms in space and time

def test_build_peptide_molsysmt_MolSys_1():
    seq = 'TyrGlyGlyPheMet'
    molsys = msm.build.build_peptide(seq, to_form='molsysmt.MolSys')
    seq_2 = msm.convert(molsys, to_form='string:aminoacids3')
    assert seq.lower()==seq_2.lower()

#def test_build_peptide_molsysmt_MolSys_2():
#    seq = 'TyrGlyGlyPheMet'
#    molsys = msm.build.build_peptide(seq, to_form=['dialanine_amber14_tip3p.prmtop','dialanine_amber14_tip3p.inpcrd'])
#    molsys = msm.convert(['dialanine_amber14_tip3p.prmtop','dialanine_amber14_tip3p.inpcrd'],
#                         to_form='molsysmt.MolSys')
#    os.remove('dialanine_amber14_tip3p.prmtop')
#    os.remove('dialanine_amber14_tip3p.inpcrd')
#    seq_2 = msm.convert(molsys, to_form='string:aminoacids3', selection='molecule_type=="peptide"')
#    is_solvated = msm.build.is_solvated(molsys)
#    check_1 = (seq.lower()==seq_2.lower())
#    check_2 = is_solvated
#    assert check_1 and check_2

