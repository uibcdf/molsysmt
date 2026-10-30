"""Testing subset fidelity for MDAnalysis AtomGroup adapters."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


def test_atomgroup_to_universe_does_not_reintroduce_parent_atoms(rich_universe):
    atom_group = rich_universe.atoms[[3, 1, 2]]

    output = msm.convert(atom_group, to_form="MDAnalysis.Universe")

    assert output.atoms.ids.tolist() == [13, 11, 12]
    assert len(output.trajectory) == 3


def test_atomgroup_molsys_subset_keeps_topology_and_coordinates_aligned(
    rich_universe,
):
    atom_group = rich_universe.atoms[[3, 1, 2]]

    output = msm.convert(
        atom_group,
        to_form="molsysmt.MolSys",
        selection=[2, 0],
        structure_indices=[2, 0],
    )

    assert output.topology.atoms["atom_id"].tolist() == ["12", "13"]
    np.testing.assert_allclose(
        puw.get_value(output.structures.coordinates, to_unit="angstrom"),
        rich_universe.trajectory.timeseries(order="fac")[[2, 0]][:, [2, 3]],
    )


def test_atomgroup_extract_applies_atoms_and_structures(rich_universe):
    atom_group = rich_universe.atoms[[3, 1, 2]]

    output = msm.extract(
        atom_group,
        selection=[1, 2],
        structure_indices=[0, 2],
        to_form="MDAnalysis.AtomGroup",
    )

    assert output.ids.tolist() == [11, 12]
    assert len(output.universe.trajectory) == 2


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize("local_selection", [[2, 0], [0, 2]])
@pytest.mark.parametrize(
    "target",
    [
        "MDAnalysis.AtomGroup",
        "MDAnalysis.Universe",
        "molsysmt.MolSys",
        "molsysmt.Topology",
    ],
)
def test_partial_reordered_group_maps_local_selection_without_changing_source(
    rich_universe, route, target, local_selection
):
    from molsysmt.form import _dict_modules, load_converter

    source = rich_universe.atoms[[3, 1, 2]]
    original = rich_universe.trajectory.timeseries(order="fac").copy()
    rich_universe.trajectory[1]
    if route == "direct":
        module = _dict_modules["MDAnalysis.AtomGroup"]
        converter = load_converter(module, module._convert_to[target])
        kwargs = {"atom_indices": local_selection}
    else:
        converter = msm.convert
        kwargs = {"to_form": target, "selection": local_selection}
    if target != "molsysmt.Topology":
        kwargs["structure_indices"] = [2, 0]

    output = converter(source, **kwargs)

    assert msm.get_form(output) == target
    if target.startswith("MDAnalysis."):
        parent_indices = source.indices[local_selection]
        atoms = output if target == "MDAnalysis.AtomGroup" else output.atoms
        assert atoms.ids.tolist() == (parent_indices + 10).tolist()
        assert atoms.names.tolist() == [f"A{i}" for i in parent_indices]
        assert atoms.universe.atoms.n_atoms == 2
        np.testing.assert_array_equal(atoms.bonds.indices, [[0, 1]])
        coordinates = atoms.universe.trajectory.timeseries(order="fac") / 10
    else:
        # Native extraction retains ascending source order; permutation is explicit.
        parent_indices = np.array([2, 3])
        topology = output.topology if target == "molsysmt.MolSys" else output
        assert topology.atoms["atom_id"].tolist() == ["12", "13"]
        assert topology.atoms["atom_name"].tolist() == ["A2", "A3"]
        assert topology.groups["group_id"].tolist() == ["7"]
        assert topology.n_groups == 1
        assert topology.n_chains == 1
        assert not hasattr(topology, "bonds")
        if target == "molsysmt.MolSys":
            np.testing.assert_array_equal(
                output.chemical_states.get_bonds()[
                    ["atom1_index", "atom2_index"]
                ].to_numpy(),
                [[0, 1]],
            )
        if target == "molsysmt.MolSys":
            coordinates = puw.get_value(output.structures.coordinates, to_unit="nm")
    if target != "molsysmt.Topology":
        assert coordinates.shape == (2, 2, 3)
        np.testing.assert_allclose(
            coordinates, original[[2, 0]][:, parent_indices] / 10
        )
    assert rich_universe.trajectory.frame == 1
    assert source.indices.tolist() == [3, 1, 2]
    np.testing.assert_array_equal(
        rich_universe.trajectory.timeseries(order="fac"), original
    )
