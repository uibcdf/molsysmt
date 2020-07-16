import pytest
from molsysmt.multitool import _get_form as get_form
from molsysmt import get
from molsysmt import convert


dict_tests={
    'pdb': 'data/1tcd.pdb',
    'pdb:id': 'pdb:1tcd',
    'molsysmt.MolSys': convert('data/1tcd.pdb', to_form='molsysmt.MolSys'),
    'molsysmt.Topology': convert('data/1tcd.pdb', to_form='molsysmt.Topology'),
    'openmm.Topology': convert('data/1tcd.pdb', to_form='openmm.Topology'),
    'openmm.Modeller': convert('data/1tcd.pdb', to_form='openmm.Modeller'),
    'openmm.PDBFile': convert('data/1tcd.pdb', to_form='openmm.PDBFile'),
    'pdbfixer.PDBFixer': convert('data/1tcd.pdb', to_form='pdbfixer.PDBFixer')

}

id_names = []
args = []

for expected, item in dict_tests.items():
    id_names.append(expected)
    args.append((item, expected))

@pytest.mark.parametrize("item,expected", args, ids=id_names)
def test_1(item, expected):
    assert get_form(item)==expected

@pytest.mark.parametrize("item,expected", args, ids=id_names)
def test_2(item, expected):
    assert get(item, target='atom', form=True)==expected

@pytest.mark.parametrize("item,expected", args, ids=id_names)
def test_3(item, expected):
    assert get(item, target='system', form=True)==expected

