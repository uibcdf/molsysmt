"""
Parity tests for file:topology_yaml form.

Oracle: builder_pdb_molsys (4 atoms, 2 groups, 1 chain, 2 bonds).
Parity means that get() on a file:topology_yaml returns identical values
to get() on the source Topology for all documented topological attributes.
"""

import pytest
import molsysmt as msm


@pytest.fixture()
def yaml_file(builder_pdb_molsys, tmp_path):
    path = str(tmp_path / 'parity.yaml')
    msm.convert(builder_pdb_molsys.topology, to_form='file:topology_yaml', output_filename=path)
    return path


@pytest.fixture()
def source_topology(builder_pdb_molsys):
    return builder_pdb_molsys.topology


# ---------------------------------------------------------------------------
# Parity: file:topology_yaml get() == Topology get() on the same system
# ---------------------------------------------------------------------------

def test_parity_n_atoms(yaml_file, source_topology):
    assert msm.get(yaml_file, element='system', n_atoms=True) == source_topology.n_atoms


def test_parity_n_groups(yaml_file, source_topology):
    assert msm.get(yaml_file, element='system', n_groups=True) == source_topology.n_groups


def test_parity_n_chains(yaml_file, source_topology):
    assert msm.get(yaml_file, element='system', n_chains=True) == source_topology.n_chains


def test_parity_n_bonds(yaml_file, source_topology):
    assert msm.get(yaml_file, element='system', n_bonds=True) == source_topology.n_bonds


def test_parity_atom_names(yaml_file, source_topology):
    assert (msm.get(yaml_file, element='atom', atom_name=True) ==
            source_topology.atoms['atom_name'].tolist())


def test_parity_group_names(yaml_file, source_topology):
    assert (msm.get(yaml_file, element='group', group_name=True) ==
            source_topology.groups['group_name'].tolist())


def test_parity_chain_ids(yaml_file, source_topology):
    assert (msm.get(yaml_file, element='chain', chain_id=True) ==
            source_topology.chains['chain_id'].tolist())
