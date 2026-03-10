import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt.native.molsys import MolSys
from tests.native.test_topology_operations import build_minimal_topology


def build_minimal_molsys(n_structures=2):
    molsys = MolSys(skip_digestion=True)
    molsys.topology = build_minimal_topology()
    molsys.structures.coordinates = puw.quantity(np.arange(n_structures * 4 * 3, dtype=np.float64).reshape((n_structures, 4, 3)), 'nm')
    molsys.structures.structure_id = np.array([str(ii) for ii in range(n_structures)], dtype=object)
    return molsys


def test_extract_can_return_self_or_copy_for_all():
    molsys = build_minimal_molsys()

    assert molsys.extract(copy_if_all=False, skip_digestion=True) is molsys
    extracted = molsys.extract(copy_if_all=True, skip_digestion=True)
    assert extracted is not molsys
    assert extracted.topology.n_atoms == molsys.topology.n_atoms
    assert extracted.structures.coordinates.shape == molsys.structures.coordinates.shape


def test_extract_subsets_atoms_and_structures():
    molsys = build_minimal_molsys(n_structures=3)
    extracted = molsys.extract(atom_indices=[0, 1], structure_indices=[1], skip_digestion=True)

    assert extracted.topology.n_atoms == 2
    assert extracted.structures.coordinates.shape == (1, 2, 3)
    assert extracted.structures.structure_id.tolist() == ['1']


def test_remove_atoms_and_structures():
    molsys = build_minimal_molsys(n_structures=3)
    trimmed = molsys.remove(atom_indices=[2, 3], structure_indices=[0, 2], skip_digestion=True)

    assert trimmed.topology.n_atoms == 2
    assert trimmed.structures.coordinates.shape == (1, 2, 3)
    assert trimmed.structures.structure_id.tolist() == ['1']


def test_add_appends_topology_and_structures():
    left = build_minimal_molsys(n_structures=1)
    right = build_minimal_molsys(n_structures=1)

    left.add(right, keep_ids=False, skip_digestion=True)

    assert left.topology.n_atoms == 8
    assert left.structures.coordinates.shape == (1, 8, 3)
    assert left.topology.atoms['atom_id'].map(type).eq(str).all()


def test_append_structures_only_grows_structure_axis():
    left = build_minimal_molsys(n_structures=1)
    right = build_minimal_molsys(n_structures=2)

    left.append_structures(right, skip_digestion=True)

    assert left.topology.n_atoms == 4
    assert left.structures.coordinates.shape == (3, 4, 3)


def test_copy_is_independent():
    molsys = build_minimal_molsys(n_structures=1)
    cloned = molsys.copy()

    cloned.topology.atoms.at[0, 'atom_name'] = 'X'
    puw.get_value(cloned.structures.coordinates)[0, 0, 0] = -1.0

    assert molsys.topology.atoms.at[0, 'atom_name'] == 'N'
    assert puw.get_value(molsys.structures.coordinates)[0, 0, 0] != -1.0


def test_rebuild_wrappers_delegate_to_topology():
    molsys = build_minimal_molsys(n_structures=1)
    molsys.topology.groups['group_type'] = np.nan
    molsys.topology.components = molsys.topology.components.iloc[0:0].copy()
    molsys.topology.molecules = molsys.topology.molecules.iloc[0:0].copy()
    molsys.topology.entities = molsys.topology.entities.iloc[0:0].copy()
    molsys.topology.chains = molsys.topology.chains.iloc[0:0].copy()
    molsys.topology.atoms['component_index'] = np.nan
    molsys.topology.atoms['chain_index'] = np.nan
    molsys.topology.groups['molecule_index'] = np.nan

    molsys.rebuild_groups(redefine_ids=True, redefine_types=True)
    molsys.rebuild_components(redefine_ids=True, redefine_types=True)
    molsys.rebuild_molecules(redefine_ids=True, redefine_types=True)
    molsys.rebuild_chains(redefine_ids=True, redefine_types=True)
    molsys.rebuild_entities(redefine_ids=True, redefine_types=True)

    assert molsys.topology.groups['group_type'].isnull().sum() == 0
    assert molsys.topology.components.shape[0] > 0
    assert molsys.topology.molecules.shape[0] > 0
    assert molsys.topology.chains.shape[0] > 0
    assert molsys.topology.entities.shape[0] > 0


def test_to_form_returns_topology_and_get_proxy_work():
    molsys = build_minimal_molsys(n_structures=1)

    topology = molsys.to_form('molsysmt.Topology', skip_digestion=True)
    atom_names = molsys.get(element='atom', atom_name=True, skip_digestion=True)

    assert topology.n_atoms == molsys.topology.n_atoms
    assert atom_names == ['N', 'CA', 'O', 'H']
