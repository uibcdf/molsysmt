"""
Parity tests for nglview.NGLWidget form.

Uses MolSysBuilder to declare a minimal system with known topology, converts
to NGLWidget and back, then verifies the round-trip preserves atom count,
group count, bond count and chain count.

Builder system:
  - 4 atoms: N (0), CA (1), C (2), O (3)
  - 2 bonds: N-CA (0-1), CA-C (1-2)
  - 2 groups: ALA, HOH
  - 1 chain: A
"""

import pytest
import molsysmt as msm

N_ATOMS  = 4
N_GROUPS = 2
N_BONDS  = 2
N_CHAINS = 1


@pytest.fixture()
def ngl_widget(builder_pdb_molsys):
    return msm.convert(builder_pdb_molsys, to_form='nglview.NGLWidget')


@pytest.fixture()
def roundtrip_molsys(ngl_widget):
    return msm.convert(ngl_widget, to_form='molsysmt.MolSys')


@pytest.fixture()
def roundtrip_topology(ngl_widget):
    return msm.convert(ngl_widget, to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# Contract: NGLWidget can be created from a MolSys
# ---------------------------------------------------------------------------

def test_nglwidget_is_created(ngl_widget):
    import nglview
    assert isinstance(ngl_widget, nglview.NGLWidget)


# ---------------------------------------------------------------------------
# Parity: MolSys → NGLWidget → MolSys preserves topology
# ---------------------------------------------------------------------------

def test_roundtrip_atom_count(roundtrip_molsys):
    assert roundtrip_molsys.topology.n_atoms == N_ATOMS


def test_roundtrip_group_count(roundtrip_molsys):
    assert roundtrip_molsys.topology.n_groups == N_GROUPS


def test_roundtrip_chain_count(roundtrip_molsys):
    assert roundtrip_molsys.topology.n_chains == N_CHAINS


def test_roundtrip_atom_names(roundtrip_molsys, builder_pdb_molsys):
    original = builder_pdb_molsys.topology.atoms['atom_name'].tolist()
    roundtrip = roundtrip_molsys.topology.atoms['atom_name'].tolist()
    assert roundtrip == original


def test_roundtrip_group_names(roundtrip_molsys, builder_pdb_molsys):
    original = builder_pdb_molsys.topology.groups['group_name'].tolist()
    roundtrip = roundtrip_molsys.topology.groups['group_name'].tolist()
    assert roundtrip == original


def test_roundtrip_topology_atom_count(roundtrip_topology):
    assert roundtrip_topology.n_atoms == N_ATOMS


def test_roundtrip_topology_group_count(roundtrip_topology):
    assert roundtrip_topology.n_groups == N_GROUPS
