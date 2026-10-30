"""
Contract and parity tests for MDAnalysis.Topology form.

MDAnalysis.Topology is the internal topology object inside an MDAnalysis
Universe.  It is created by parsing a PDB file via
msm.convert(pdb_path, to_form='MDAnalysis.Topology').

Oracle: 1l2y.pdb (Trp-cage, 304 atoms, 20 residues, 1 chain).

Contract: MDAnalysis.Topology can be created and its native attributes
(n_atoms, n_residues, n_segments) match the expected oracle counts.

Parity: MDAnalysis.Topology → molsysmt.Topology preserves atom count,
group count, chain count, atom names, and group names.
"""

from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm

PDB_PATH = str(Path(msm.__file__).parent / "data" / "pdb" / "1l2y.pdb")
N_ATOMS = 304
N_RESIDUES = 20
N_SEGMENTS = 1


@pytest.fixture(scope="module")
def mda_topology():
    return msm.convert(PDB_PATH, to_form="MDAnalysis.Topology")


@pytest.fixture(scope="module")
def source_topology():
    return msm.convert(PDB_PATH, to_form="molsysmt.Topology")


@pytest.fixture(scope="module")
def roundtrip_topology(mda_topology):
    return msm.convert(mda_topology, to_form="molsysmt.Topology")


# ---------------------------------------------------------------------------
# Contract: MDAnalysis.Topology is created from a PDB file
# ---------------------------------------------------------------------------


def test_mda_topology_is_created(mda_topology):
    from MDAnalysis.core.topology import Topology

    assert isinstance(mda_topology, Topology)


def test_mda_topology_atom_count(mda_topology):
    assert mda_topology.n_atoms == N_ATOMS


def test_mda_topology_residue_count(mda_topology):
    assert mda_topology.n_residues == N_RESIDUES


def test_mda_topology_segment_count(mda_topology):
    assert mda_topology.n_segments == N_SEGMENTS


# ---------------------------------------------------------------------------
# Parity: MDAnalysis.Topology → molsysmt.Topology preserves topology
# ---------------------------------------------------------------------------


def test_parity_atom_count(roundtrip_topology, source_topology):
    assert roundtrip_topology.n_atoms == source_topology.n_atoms


def test_parity_group_count(roundtrip_topology, source_topology):
    assert roundtrip_topology.n_groups == source_topology.n_groups


def test_parity_chain_count(roundtrip_topology, source_topology):
    assert roundtrip_topology.n_chains == source_topology.n_chains


def test_parity_atom_names(roundtrip_topology, source_topology):
    assert (
        roundtrip_topology.atoms["atom_name"].tolist()
        == source_topology.atoms["atom_name"].tolist()
    )


def test_parity_group_names(roundtrip_topology, source_topology):
    assert (
        roundtrip_topology.groups["group_name"].tolist()
        == source_topology.groups["group_name"].tolist()
    )


def test_topology_self_conversion_applies_atom_subset(mda_topology):
    output = msm.convert(
        mda_topology,
        to_form="MDAnalysis.Topology",
        selection=[2, 0],
    )

    assert output.n_atoms == 2
    assert output.ids.values.tolist() == [3, 1]


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize(
    "target", ["MDAnalysis.Topology", "molsysmt.Topology", "molsysmt.MolSys"]
)
def test_topology_reordering_preserves_labels_and_connectivity(
    rich_universe, route, target
):
    from molsysmt.form import _dict_modules, load_converter

    source = rich_universe._topology.copy()
    if route == "direct":
        module = _dict_modules["MDAnalysis.Topology"]
        converter = load_converter(module, module._convert_to[target])
        output = converter(source, atom_indices=[3, 2])
    else:
        output = msm.convert(source, to_form=target, selection=[3, 2])

    assert msm.get_form(output) == target
    if target == "MDAnalysis.Topology":
        assert output.ids.values.tolist() == [13, 12]
        assert output.names.values.tolist() == ["A3", "A2"]
        assert output.resids.values.tolist() == [7]
        np.testing.assert_array_equal(output.bonds.values, [[0, 1]])
    else:
        # Native extraction retains ascending source order; permutation is explicit.
        inventory = output.topology if target == "molsysmt.MolSys" else output
        assert inventory.atoms["atom_id"].tolist() == ["12", "13"]
        assert inventory.atoms["atom_name"].tolist() == ["A2", "A3"]
        assert inventory.groups["group_id"].tolist() == ["7"]
        if target == "molsysmt.MolSys":
            np.testing.assert_array_equal(
                output.chemical_states.get_bonds()[
                    ["atom1_index", "atom2_index"]
                ].to_numpy(),
                [[0, 1]],
            )
        else:
            assert not hasattr(output, "bonds")
    assert msm.get(output, n_atoms=True) == 2
    assert source.n_atoms == 4
    assert source.ids.values.tolist() == [10, 11, 12, 13]
    np.testing.assert_array_equal(source.bonds.values, [(0, 1), (1, 2), (2, 3)])
