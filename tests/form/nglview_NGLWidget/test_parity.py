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


def test_nglwidget_does_not_claim_metadata_it_cannot_preserve(ngl_widget):
    available = msm.get_attributes(ngl_widget)

    assert 'occupancy' not in available
    assert 'temperature' not in available
    assert 'potential_energy' not in available
    assert 'kinetic_energy' not in available
    assert 'total_energy' not in available


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


def test_molsysmt_widget_preserves_exact_topology_sidecar(builder_pdb_molsys):
    source = builder_pdb_molsys.copy()
    source.topology.atoms["atom_id"] = ["7", "7", "A", "42"]
    source.topology.bonds["bond_type"] = ["covalent", "dative"]

    widget = msm.convert(source, to_form="nglview.NGLWidget")
    observed = msm.convert(widget, to_form="molsysmt.Topology")

    assert observed.atoms["atom_id"].tolist() == ["7", "7", "A", "42"]
    assert observed.bonds["bond_type"].tolist() == ["covalent", "dative"]


def test_molsysmt_widget_topology_is_an_isolated_snapshot(builder_pdb_molsys):
    source = builder_pdb_molsys.copy()
    expected = source.topology.atoms["atom_id"].tolist()
    widget = msm.convert(source, to_form="nglview.NGLWidget")

    source.topology.atoms["atom_id"] = ["changed"] * source.topology.n_atoms
    observed = msm.convert(widget, to_form="molsysmt.Topology")

    assert observed.atoms["atom_id"].tolist() == expected


def test_empty_external_widget_does_not_claim_topology():
    import nglview

    widget = nglview.NGLWidget()

    assert not msm.has_attribute(widget, "atom_id")
    assert not msm.has_attribute(widget, "bond_type")


def test_external_pdb_widget_uses_limited_fallback(builder_pdb_molsys):
    import nglview

    pdb_text = msm.convert(builder_pdb_molsys, to_form="string:pdb_text")
    widget = nglview.show_text(pdb_text)

    assert msm.has_attribute(widget, "atom_id")
    assert not msm.has_attribute(widget, "bond_type")
    assert msm.get(widget, n_atoms=True) == N_ATOMS


def test_multicomponent_widget_does_not_claim_single_component_sidecar(
    builder_pdb_molsys,
):
    widget = msm.convert(builder_pdb_molsys, to_form="nglview.NGLWidget")
    pdb_text = msm.convert(builder_pdb_molsys, to_form="string:pdb_text")
    widget.add_component(pdb_text, ext="pdb")

    assert not msm.has_attribute(widget, "bond_type")
