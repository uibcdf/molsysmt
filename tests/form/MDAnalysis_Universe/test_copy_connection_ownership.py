"""Keeping public connection edits independent after MDAnalysis copying."""

import numpy as np
import pytest

import molsysmt as msm


def _universe(trajectory):
    mda = pytest.importorskip("MDAnalysis")
    from MDAnalysis.core.topologyattrs import Bonds

    universe = mda.Universe.empty(
        3, n_residues=1, atom_resindex=[0, 0, 0], trajectory=trajectory
    )
    universe.add_TopologyAttr("names", ["C", "N", "O"])
    universe.add_TopologyAttr("types", ["C", "N", "O"])
    universe.add_TopologyAttr("ids", [10, 11, 12])
    universe.add_TopologyAttr("resnames", ["LIG"])
    universe.add_TopologyAttr("resids", [7])
    universe.add_TopologyAttr("segids", ["A"])
    universe.add_TopologyAttr(
        Bonds(
            [(0, 1)],
            types=["original long opaque type"],
            guessed=[True],
            order=[1.5],
        )
    )
    return universe


def _assert_independent_public_bond_addition(source, output):
    frame = source.trajectory.frame if hasattr(source, "trajectory") else None

    output.add_bonds(
        [(1, 2)], types=["new independent long type"], guessed=[False], order=[2]
    )

    original = source._topology.bonds
    assert list(map(tuple, original.values)) == [(0, 1)]
    assert list(original.types) == ["original long opaque type"]
    assert list(original.order) == [1.5]
    assert list(original._guessed) == [True]
    np.testing.assert_array_equal(source.atoms.ids, [10, 11, 12])
    if frame is not None:
        assert source.trajectory.frame == frame

    changed = output._topology.bonds
    assert list(map(tuple, changed.values)) == [(0, 1), (1, 2)]
    assert list(changed.types) == [
        "original long opaque type",
        "new independent long type",
    ]
    assert list(changed.order) == [1.5, 2]
    assert list(changed._guessed) == [True, False]


@pytest.mark.parametrize("trajectory", [False, True])
@pytest.mark.parametrize("source_kind", ["universe", "atomgroup"])
def test_public_copy_detaches_connection_annotations_for_later_edits(
    trajectory, source_kind
):
    source = _universe(trajectory)
    item = source if source_kind == "universe" else source.atoms[[2, 0]]

    copied = msm.copy(item)

    assert copied.atoms.universe is not source
    if source_kind == "atomgroup":
        assert copied.indices.tolist() == [2, 0]
        assert copied.universe.atoms.n_atoms == 3
    _assert_independent_public_bond_addition(source, copied.atoms.universe)


@pytest.mark.parametrize("operation", ["extract", "same_form"])
@pytest.mark.parametrize("selection_kind", ["topology_only", "all", "structures"])
def test_all_atom_operations_detach_connection_annotations_for_later_edits(
    operation, selection_kind
):
    source = _universe(selection_kind != "topology_only")
    options = {"structure_indices": [0]} if selection_kind == "structures" else {}

    if operation == "extract":
        output = msm.extract(source, **options)
    else:
        output = msm.convert(source, to_form="MDAnalysis.Universe", **options)

    assert output is not source
    assert hasattr(output, "trajectory") == hasattr(source, "trajectory")
    _assert_independent_public_bond_addition(source, output)
