"""Protect public bond queries on TopoMT geometric systems without bonds."""

from pathlib import Path

import pytest

import molsysmt as msm
from molsysmt.native import Topology

FIXTURE = Path(__file__).parent / "data" / "topomt_geometric_tetrahedron.pdb"


@pytest.fixture(scope="module")
def geometric_system():
    return msm.convert(str(FIXTURE), to_form="molsysmt.MolSys")


@pytest.mark.parametrize("form", ["molsysmt.MolSys", "molsysmt.Topology", "file:pdb"])
@pytest.mark.parametrize("selection,n_selected", [("all", 4), ([1, 3], 2), ([], 0)])
def test_empty_bond_indices_and_zero_atom_counts(
    geometric_system, form, selection, n_selected
):
    source = (
        str(FIXTURE)
        if form == "file:pdb"
        else msm.convert(geometric_system, to_form=form)
    )
    assert (
        msm.get(source, element="atom", selection=selection, n_bonds=True)
        == [0] * n_selected
    )
    assert msm.get(source, element="atom", selection=selection, bond_index=True) == [
        [] for _ in range(n_selected)
    ]
    assert msm.get(
        source, element="atom", selection=selection, inner_bond_index=True
    ) == [[] for _ in range(n_selected)]
    # The file adapter does not advertise this pair attribute; keep its None result.
    expected_pairs = None if form == "file:pdb" else []
    assert (
        msm.get(source, element="atom", selection=selection, bonded_atom_pairs=True)
        == expected_pairs
    )
    assert msm.get(source, element="system", n_bonds=True) == 0
    assert msm.get(source, element="system", bond_index=True) == []
    assert msm.get(source, n_atoms=True) == 4


@pytest.mark.parametrize(
    "element", ["group", "component", "molecule", "chain", "entity"]
)
def test_empty_bonds_remain_empty_at_aggregate_levels(element):
    builder = msm.MolSysBuilder()
    atoms = [builder.add_atom(atom_name="C", atom_type="C") for _ in range(4)]
    group = builder.add_group(atoms, group_name="DUM", group_type="unknown")
    builder.add_chain([group], chain_id="A", chain_name="A", chain_type="unknown")
    molecule = builder.add_molecule([group], molecule_type="unknown")
    builder.add_entity([molecule], entity_type="unknown")
    topology = builder.build().topology
    indices = msm.get(topology, element=element, **{f"{element}_index": True})
    result = msm.get(
        topology,
        element=element,
        output_type="dictionary",
        n_bonds=True,
        bond_index=True,
        inner_bond_index=True,
    )
    assert result["n_bonds"] == [0] * len(indices)
    assert result["bond_index"] == [[] for _ in indices]
    assert result["inner_bond_index"] == [[] for _ in indices]


def test_zero_atom_topology_has_empty_outputs():
    topology = Topology(n_atoms=0)
    result = msm.get(
        topology,
        element="atom",
        output_type="dictionary",
        n_bonds=True,
        bond_index=True,
        inner_bond_index=True,
        bonded_atom_pairs=True,
    )
    assert result == {
        "n_bonds": [],
        "bond_index": [],
        "inner_bond_index": [],
        "bonded_atom_pairs": [],
    }


def test_existing_bond_indices_and_selected_inner_scopes_are_preserved():
    builder = msm.MolSysBuilder()
    atoms = [builder.add_atom(atom_name="C", atom_type="C") for _ in range(4)]
    builder.add_bond(atoms[0], atoms[1])
    builder.add_bond(atoms[1], atoms[2])
    source = builder.build()
    assert msm.get(source, element="atom", bond_index=True) == [[0], [0, 1], [1], []]
    assert msm.get(source, element="atom", selection=[1, 3], n_bonds=True) == [2, 0]
    assert msm.get(source, element="atom", selection=[1, 3], inner_bond_index=True) == [
        [],
        [],
    ]
    assert msm.get(source, element="atom", selection=[0, 1], inner_bond_index=True) == [
        [0],
        [0],
    ]
    assert msm.get(
        source, element="atom", selection=[1, 3], bonded_atom_pairs=True
    ) == [[0, 1], [1, 2]]
