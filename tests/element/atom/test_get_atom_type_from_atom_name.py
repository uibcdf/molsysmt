"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm


def test_atom_type_from_atom_name_1():
    assert 'H' == msm.element.atom.get_atom_type_from_atom_name('H1')
    assert 'C' == msm.element.atom.get_atom_type_from_atom_name('CB')
    assert 'O' == msm.element.atom.get_atom_type_from_atom_name('O2')
    assert 'N' == msm.element.atom.get_atom_type_from_atom_name('N')

def test_atom_type_from_atom_name_2():
    assert 'UNK' == msm.element.atom.get_atom_type_from_atom_name('XXX')
