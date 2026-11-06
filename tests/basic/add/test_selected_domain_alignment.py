"""Preserving selected atom identities across native addition domains (#618)."""

import warnings

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import (
    ArgumentError,
    BioassemblyIdentifierCollisionWarning,
    StructuralInconsistencyError,
)
from molsysmt.native import MolSys


def _system(n_atoms, prefix, n_structures=2):
    system = MolSys(
        n_atoms=n_atoms,
        n_groups=n_atoms,
        n_molecules=n_atoms,
        n_entities=n_atoms,
        n_chains=n_atoms,
    )
    for level, plural in (
        ("atom", "atoms"),
        ("group", "groups"),
        ("molecule", "molecules"),
        ("entity", "entities"),
        ("chain", "chains"),
    ):
        table = getattr(system.topology, plural)
        table[level + "_id"] = pd.array(
            [f"{prefix}{i}" for i in range(n_atoms)], dtype="string"
        )
        table[level + "_name"] = [f"{prefix}{i}" for i in range(n_atoms)]
    for child, parent in (
        ("atoms", "group"),
        ("atoms", "chain"),
        ("groups", "molecule"),
        ("molecules", "entity"),
    ):
        getattr(system.topology, child)[parent + "_index"] = pd.array(
            range(n_atoms), dtype="Int64"
        )
    system.topology.atoms["atom_type"] = ["C"] * n_atoms
    # These charges/types are index markers, not a parameterized physical model.
    msm.set(system, element="atom", formal_charge=list(range(n_atoms)))
    if n_atoms > 1:
        system.chemical_states.add_bonds([[0, n_atoms - 1]])
        msm.set(system, element="bond", bond_order=[1])
    system.chemical_states.rebuild_components(topology=system.topology)
    values = np.arange(n_structures * n_atoms * 3, dtype=float).reshape(
        n_structures, n_atoms, 3
    )
    system.structures.coordinates = puw.quantity(values, "angstrom")
    system.structures.velocities = puw.quantity(values + 100, "angstrom/ps")
    system.structures.b_factor = puw.quantity(values[:, :, 0] + 200, "nm**2")
    system.structures.occupancy = values[:, :, 0] / 1000
    system.structures.alternate_location = [
        {i: f"{prefix}{i}" for i in range(n_atoms)} for _ in range(n_structures)
    ]
    system.molecular_mechanics.partial_charge = np.arange(n_atoms, dtype=float)
    system.molecular_mechanics.atom_ff_type = [f"{prefix}{i}" for i in range(n_atoms)]
    return system


def _add(target, source, selection, route, in_place):
    if route == "public":
        result = msm.add(target, source, selection=selection, in_place=in_place)
        return target if in_place else result
    output = target if in_place else target.copy()
    if route == "native":
        output.add(source, atom_indices=selection)
    else:
        from molsysmt.form.molsysmt_MolSys.add import add

        add(output, source, atom_indices=selection)
    return output


@pytest.mark.parametrize("route", ["public", "native", "adapter"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("selection", [[2, 0], [2, 1, 0], [], "all"])
def test_selected_add_keeps_atom_identity_in_every_domain(route, in_place, selection):
    target, source = _system(1, "L"), _system(3, "R")
    source_before = source.copy()
    target_before = target.copy()
    expected_indices = np.array(
        [0, 1, 2] if isinstance(selection, str) else sorted(selection), dtype=int
    )

    output = _add(target, source, selection, route, in_place)

    assert output.topology.atoms["atom_name"].tolist() == ["L0"] + [
        f"R{i}" for i in expected_indices
    ]
    assert output.topology.atoms["atom_id"].tolist() == ["L0"] + [
        f"R{i}" for i in expected_indices
    ]
    for field, unit in (("coordinates", "nm"), ("velocities", "nm/ps")):
        expected = np.concatenate(
            [
                puw.get_value(getattr(target_before.structures, field), to_unit=unit),
                puw.get_value(getattr(source.structures, field), to_unit=unit)[
                    :, expected_indices
                ],
            ],
            axis=1,
        )
        np.testing.assert_allclose(
            puw.get_value(getattr(output.structures, field), to_unit=unit), expected
        )
    for field in ("b_factor", "occupancy"):
        output_values = getattr(output.structures, field)
        left_values = getattr(target_before.structures, field)
        right_values = getattr(source.structures, field)
        if field == "b_factor":
            output_values = puw.get_value(output_values, to_unit="nm**2")
            left_values = puw.get_value(left_values, to_unit="nm**2")
            right_values = puw.get_value(right_values, to_unit="nm**2")
        np.testing.assert_array_equal(
            output_values,
            np.concatenate(
                [left_values, right_values[:, expected_indices]],
                axis=1,
            ),
        )
    expected_markers = [0, *expected_indices.tolist()]
    assert msm.get(output, element="atom", formal_charge=True) == expected_markers
    np.testing.assert_array_equal(
        output.molecular_mechanics.partial_charge, expected_markers
    )
    assert output.molecular_mechanics.atom_ff_type.tolist() == ["L0"] + [
        f"R{i}" for i in expected_indices
    ]
    bonds = output.chemical_states.get_bonds()
    expected_pairs = (
        [[1, len(expected_indices)]]
        if 0 in expected_indices and 2 in expected_indices
        else []
    )
    np.testing.assert_array_equal(
        bonds[["atom1_index", "atom2_index"]].to_numpy(dtype=int),
        np.asarray(expected_pairs, dtype=int).reshape(-1, 2),
    )
    membership = np.asarray(msm.get(output, element="atom", component_index=True))
    assert len(membership) == output.topology.n_atoms
    if expected_pairs:
        assert membership[1] == membership[-1]
        assert membership[0] != membership[1]
    expected_alt = {
        0: "L0",
        **{i + 1: f"R{old}" for i, old in enumerate(expected_indices)},
    }
    assert output.structures.alternate_location == [expected_alt, expected_alt]
    pd.testing.assert_frame_equal(source.topology.atoms, source_before.topology.atoms)
    pd.testing.assert_frame_equal(
        source.molecular_mechanics.atoms_ff, source_before.molecular_mechanics.atoms_ff
    )
    np.testing.assert_equal(
        puw.get_value(source.structures.coordinates, to_unit="nm"),
        puw.get_value(source_before.structures.coordinates, to_unit="nm"),
    )
    if not in_place:
        pd.testing.assert_frame_equal(
            target.topology.atoms, target_before.topology.atoms
        )
        pd.testing.assert_frame_equal(
            target.molecular_mechanics.atoms_ff,
            target_before.molecular_mechanics.atoms_ff,
        )


def _assemblies():
    return {
        "keep": {
            "chain_indices": [2],
            "rotations": np.eye(3)[None],
            "translations": np.zeros((1, 3)),
        },
        "drop": {
            "chain_indices": [1],
            "rotations": np.eye(3)[None],
            "translations": np.zeros((1, 3)),
        },
        "operations": {
            "chain_indices": [[0], [1, 2], [2]],
            "rotations": np.repeat(np.eye(3)[None], 3, axis=0),
            "translations": np.arange(9).reshape(3, 3),
        },
    }


def test_selected_add_projects_bioassembly_chains_and_operations_independently():
    target, source = _system(1, "L"), _system(3, "R")
    source.structures.bioassembly = _assemblies()

    result = msm.add(target, source, selection=[2, 0], in_place=False)

    assemblies = result.structures.bioassembly
    assert set(assemblies) == {"keep", "operations"}
    assert assemblies["keep"]["chain_indices"] == [2]
    assert assemblies["operations"]["chain_indices"] == [[1], [2]]
    np.testing.assert_array_equal(
        assemblies["operations"]["translations"], [[0, 1, 2], [6, 7, 8]]
    )
    assemblies["keep"]["translations"][0, 0] = 99
    assert source.structures.bioassembly["keep"]["translations"][0, 0] == 0


@pytest.mark.parametrize("structure_indices", [[2, 0], [2, 2]])
def test_selected_add_keeps_structure_order_and_repetitions(structure_indices):
    target, source = _system(1, "L"), _system(3, "R", n_structures=3)

    result = msm.add(
        target,
        source,
        selection=[2, 0],
        structure_indices=structure_indices,
        in_place=False,
    )

    actual = puw.get_value(result.structures.coordinates, to_unit="nm")
    expected = puw.get_value(source.structures.coordinates, to_unit="nm")
    np.testing.assert_allclose(
        actual[:, 1:], expected[np.ix_(structure_indices, [0, 2], [0, 1, 2])]
    )
    assert result.structures.alternate_location == [
        {0: "L0", 1: "R0", 2: "R2"},
        {0: "L0", 1: "R0", 2: "R2"},
    ]


def test_selected_add_without_structures_keeps_chemical_and_mechanical_axes():
    target, source = _system(1, "L"), _system(3, "R")
    target.structures = None
    source.structures = None

    target.add(source, atom_indices=[2, 0])

    assert target.structures is None
    assert target.topology.atoms["atom_name"].tolist() == ["L0", "R0", "R2"]
    assert msm.get(target, element="atom", formal_charge=True) == [0, 0, 2]
    assert target.molecular_mechanics.atom_ff_type.tolist() == ["L0", "R0", "R2"]


@pytest.mark.parametrize("selection", [[2, 2], [-1], [3]])
def test_invalid_native_add_selection_rejects_without_publishing(selection):
    target, source = _system(1, "L"), _system(3, "R")
    before = target.copy()
    with pytest.raises(ArgumentError, match="atom_indices"):
        target.add(source, atom_indices=selection)
    pd.testing.assert_frame_equal(target.topology.atoms, before.topology.atoms)
    pd.testing.assert_frame_equal(
        target.molecular_mechanics.atoms_ff, before.molecular_mechanics.atoms_ff
    )
    np.testing.assert_array_equal(
        puw.get_value(target.structures.coordinates, to_unit="nm"),
        puw.get_value(before.structures.coordinates, to_unit="nm"),
    )


def test_selected_add_retains_atomic_unsupported_state_rejection():
    target, source = _system(1, "L"), _system(3, "R")
    source.chemical_states.append_state()
    before = target.copy()
    with pytest.raises(StructuralInconsistencyError, match="one chemical state"):
        target.add(source, atom_indices=[2, 0])
    pd.testing.assert_frame_equal(target.topology.atoms, before.topology.atoms)
    pd.testing.assert_frame_equal(
        target.molecular_mechanics.atoms_ff, before.molecular_mechanics.atoms_ff
    )


def test_selected_bioassembly_collision_warning_as_error_is_atomic():
    target, source = _system(1, "L"), _system(3, "R")
    target.structures.bioassembly = {
        "keep": _assemblies()["operations"] | {"chain_indices": [0]}
    }
    source.structures.bioassembly = _assemblies()
    before = target.copy()
    with warnings.catch_warnings():
        warnings.simplefilter("error", BioassemblyIdentifierCollisionWarning)
        with pytest.raises(BioassemblyIdentifierCollisionWarning):
            target.add(source, atom_indices=[2, 0])
    pd.testing.assert_frame_equal(target.topology.atoms, before.topology.atoms)
    pd.testing.assert_frame_equal(
        target.molecular_mechanics.atoms_ff, before.molecular_mechanics.atoms_ff
    )
    np.testing.assert_array_equal(
        puw.get_value(target.structures.coordinates, to_unit="nm"),
        puw.get_value(before.structures.coordinates, to_unit="nm"),
    )
