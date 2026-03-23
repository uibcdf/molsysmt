"""
Parity tests for molsysmt.TopologyDict form.

Oracle: builder_pdb_molsys (4 atoms, 2 groups, 1 chain, 2 bonds).
Parity means that get() on a TopologyDict returns identical values to
get() on the original Topology for all documented topological attributes.
"""

import pytest
import molsysmt as msm


@pytest.fixture()
def source_topology(builder_pdb_molsys):
    return builder_pdb_molsys.topology


@pytest.fixture()
def topology_dict(builder_pdb_molsys):
    return msm.convert(builder_pdb_molsys.topology, to_form='molsysmt.TopologyDict')


# ---------------------------------------------------------------------------
# Parity: TopologyDict get() == Topology get() on the same system
# ---------------------------------------------------------------------------

def test_parity_n_atoms(topology_dict, source_topology):
    assert (msm.get(topology_dict, element='system', n_atoms=True) ==
            source_topology.n_atoms)


def test_parity_n_groups(topology_dict, source_topology):
    assert (msm.get(topology_dict, element='system', n_groups=True) ==
            source_topology.n_groups)


def test_parity_n_chains(topology_dict, source_topology):
    assert (msm.get(topology_dict, element='system', n_chains=True) ==
            source_topology.n_chains)


def test_parity_n_bonds(topology_dict, source_topology):
    assert (msm.get(topology_dict, element='system', n_bonds=True) ==
            source_topology.n_bonds)


def test_parity_atom_names(topology_dict, source_topology):
    assert (msm.get(topology_dict, element='atom', atom_name=True) ==
            source_topology.atoms['atom_name'].tolist())


def test_parity_group_names(topology_dict, source_topology):
    assert (msm.get(topology_dict, element='group', group_name=True) ==
            source_topology.groups['group_name'].tolist())


def test_parity_chain_ids(topology_dict, source_topology):
    assert (msm.get(topology_dict, element='chain', chain_id=True) ==
            source_topology.chains['chain_id'].tolist())
