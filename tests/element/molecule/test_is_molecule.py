"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_is_molecule_type_molsysmt_MolSys_1():

    assert msm.element.molecule.is_molecule_type('water')
    assert msm.element.molecule.is_molecule_type('ion')
    assert msm.element.molecule.is_molecule_type('small molecule')
    assert msm.element.molecule.is_molecule_type('peptide')
    assert msm.element.molecule.is_molecule_type('protein')
    assert msm.element.molecule.is_molecule_type('dna')
    assert msm.element.molecule.is_molecule_type('rna')
    assert msm.element.molecule.is_molecule_type('lipid')
    assert msm.element.molecule.is_molecule_type('oligosaccharide')

def test_is_molecule_type_molsysmt_MolSys_2():

    assert msm.element.molecule.is_molecule_type('waters')
    assert msm.element.molecule.is_molecule_type('ions')
    assert msm.element.molecule.is_molecule_type('small molecules')
    assert msm.element.molecule.is_molecule_type('peptides')
    assert msm.element.molecule.is_molecule_type('proteins')
    assert msm.element.molecule.is_molecule_type('dnas')
    assert msm.element.molecule.is_molecule_type('rnas')
    assert msm.element.molecule.is_molecule_type('lipids')
    assert msm.element.molecule.is_molecule_type('oligosaccharides')

