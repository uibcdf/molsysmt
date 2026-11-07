"""Preserve chemical labels and dense hierarchy axes in external topology subsets."""

import pytest

import molsysmt as msm
from molsysmt.form.mdtraj_Topology.extract import extract


@pytest.fixture
def source():
    md = pytest.importorskip("mdtraj")
    topology = md.Topology()
    for chain_id, sequence, segment, names, charges in (
        ("A", 7, "LEFT", ["N", "C"], [1, 0]),
        ("B", 0, "RIGHT", ["O", "H"], [-1, None]),
    ):
        chain = topology.add_chain(chain_id=chain_id)
        group = topology.add_residue("LIG", chain, resSeq=sequence, segment_id=segment)
        for name, charge in zip(names, charges):
            topology.add_atom(
                name,
                md.element.get_by_symbol(name),
                group,
                serial=10 + topology.n_atoms,
                formal_charge=charge,
            )
    topology.add_bond(topology.atom(0), topology.atom(1), type=md.Double, order=2)
    topology.add_bond(topology.atom(1), topology.atom(2))
    topology.add_bond(topology.atom(2), topology.atom(3), type=md.Single, order=1)
    return topology


def _signature(topology):
    return (
        [(c.index, c.chain_id) for c in topology.chains],
        [
            (r.index, r.name, r.resSeq, r.segment_id, r.chain.index)
            for r in topology.residues
        ],
        [
            (a.index, a.name, a.serial, a.formal_charge, a.residue.index)
            for a in topology.atoms
        ],
        [
            (a.index, b.index, bond.type, bond.order)
            for bond in topology.bonds
            for a, b in [bond]
        ],
    )


@pytest.mark.parametrize("route", ["public", "adapter"])
@pytest.mark.parametrize("selection", [[2, 3], [1, 0], [3, 1], [], "all", [3, 2, 1, 0]])
def test_selected_metadata_dense_axes_and_source_independence(source, selection, route):
    before = _signature(source)
    result = (
        msm.extract(source, selection=selection)
        if route == "public"
        else extract(source, atom_indices=selection)
    )
    indices = [0, 1, 2, 3] if selection == "all" else sorted(selection)
    groups = sorted({i // 2 for i in indices})
    assert result.n_atoms == len(indices)
    assert [a.index for a in result.atoms] == list(range(len(indices)))
    assert [a.name for a in result.atoms] == [["N", "C", "O", "H"][i] for i in indices]
    assert [a.serial for a in result.atoms] == [10 + i for i in indices]
    assert [a.formal_charge for a in result.atoms] == [
        [1, 0, -1, None][i] for i in indices
    ]
    assert [c.index for c in result.chains] == list(range(len(groups)))
    assert [r.index for r in result.residues] == list(range(len(groups)))
    assert [c.chain_id for c in result.chains] == [["A", "B"][i] for i in groups]
    assert [r.resSeq for r in result.residues] == [[7, 0][i] for i in groups]
    assert [r.segment_id for r in result.residues] == [
        ["LEFT", "RIGHT"][i] for i in groups
    ]
    atom_map = {old: new for new, old in enumerate(indices)}
    expected = [
        (atom_map[a], atom_map[b], order)
        for a, b, order in [(0, 1, 2), (1, 2, None), (2, 3, 1)]
        if a in atom_map and b in atom_map
    ]
    assert [
        (a.index, b.index, bond.order) for bond in result.bonds for a, b in [bond]
    ] == expected
    assert [
        str(bond.type) if bond.type is not None else None for bond in result.bonds
    ] == [{2: "Double", 1: "Single", None: None}[order] for _, _, order in expected]
    assert _signature(source) == before
    native = msm.convert(result, to_form="molsysmt.MolSys")
    assert native.get(formal_charge=True) == [[1, 0, -1, None][i] for i in indices]
    if indices:
        result.atom(0).name = "changed"
        result.chain(0).chain_id = "changed"
    assert _signature(source) == before


@pytest.mark.parametrize("copy_if_all", [False, True])
def test_unrestricted_extraction_preserves_copy_policy(source, copy_if_all):
    result = extract(source, copy_if_all=copy_if_all)
    assert (result is source) == (not copy_if_all)
    assert _signature(result) == _signature(source)
