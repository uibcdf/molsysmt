"""Check sequence-guided fits against rigid poses and explicit source axes."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError


def xyz(system):
    return puw.get_value(
        msm.get(system, element="atom", coordinates=True), to_unit="nm"
    )


def pose(points, turn, shift):
    out = points.copy()
    if turn == 1:
        out[:, 0], out[:, 1] = -points[:, 1], points[:, 0]
    elif turn == 2:
        out[:, 0], out[:, 1] = -points[:, 0], -points[:, 1]
    return out + np.asarray(shift)


@pytest.fixture
def poses():
    peptide = msm.convert(
        msm.systems["pentalanine"]["traj_pentalanine.h5msm"],
        structure_indices=[0, 8, 3],
    )
    n = msm.get(peptide, n_atoms=True)
    i = np.arange(n, dtype=float)
    base = np.column_stack((i * 0.05, (i % 7) * 0.1, (i % 11) * 0.07))
    builder = msm.MolSysBuilder()
    for name, kind in [("O", "O"), ("H1", "H"), ("H2", "H")]:
        builder.add_atom(atom_name=name, atom_type=kind)
    builder.add_group([0, 1, 2], group_name="HOH", group_type="water")
    builder.add_bond(0, 1)
    builder.add_bond(0, 2)
    water = np.array([[10.0, 2.0, 1.0], [10.1, 2.0, 1.0], [10.0, 2.1, 1.0]])
    builder.set_coordinates(puw.quantity(np.tile(water[None], (3, 1, 1)), "nm"))
    spectator = builder.build()
    query = msm.merge([peptide, spectator])
    reference = msm.merge([spectator, peptide])
    query_points = np.stack(
        [
            pose(base, 1, [1.2, -0.3, 0.6]),
            pose(base, 0, [-0.5, 0.4, 0.2]),
            pose(base, 2, [0.3, 1.4, -0.8]),
        ]
    )
    reference_points = np.stack(
        [pose(base, 2, [2.0, -0.4, 0.6]), base, pose(base, 1, [-0.1, 0.8, 1.0])]
    )
    msm.set(
        query,
        coordinates=puw.quantity(
            np.concatenate([query_points, np.tile(water[None], (3, 1, 1))], axis=1),
            "nm",
        ),
    )
    msm.set(
        reference,
        coordinates=puw.quantity(
            np.concatenate([np.tile(water[None], (3, 1, 1)), reference_points], axis=1),
            "nm",
        ),
    )
    return query, reference, base, n


def atom_selection(system, representation, expression='atom_name=="CA"'):
    atoms = msm.select(system, selection=expression)
    if representation == "expression":
        return expression
    if representation == "list":
        return atoms[::-1] + atoms[:1]
    if representation == "tuple":
        return tuple(atoms[::-1])
    if representation == "array":
        return np.array(atoms[::-1], dtype=np.int32)
    mask = np.zeros(msm.get(system, n_atoms=True), dtype=bool)
    mask[atoms] = True
    return mask if representation == "mask" else mask.tolist()


@pytest.mark.parametrize("reference_mode", ["omitted", "none", "self"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("structures", [[2, 0, 2], [1], [2, 1, 0]])
@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
def test_self_reference_uses_original_selected_reference_structure(
    poses, reference_mode, in_place, structures, unit
):
    query, _, _, n = poses
    before = xyz(query).copy()
    parameters = (
        {}
        if reference_mode == "omitted"
        else {"reference_molecular_system": None if reference_mode == "none" else query}
    )
    expected = before.copy()
    expected[np.ix_(np.unique(structures), np.arange(n))] = before[1, :n]
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = msm.structure.least_rmsd_align(
            query,
            structure_indices=structures,
            reference_structure_index=1,
            in_place=in_place,
            use_gpu=False,
            **parameters,
        )
    output = query if in_place else result
    assert (result is None) == in_place
    np.testing.assert_allclose(xyz(output), expected, rtol=0, atol=1e-11)
    if not in_place:
        assert result is not query
        np.testing.assert_array_equal(xyz(query), before)


@pytest.mark.parametrize(
    "query_kind", ["expression", "list", "tuple", "array", "mask", "mask_list"]
)
@pytest.mark.parametrize(
    "reference_kind", ["expression", "list", "tuple", "array", "mask", "mask_list"]
)
@pytest.mark.parametrize("in_place", [False, True])
def test_atomic_population_representations_preserve_group_and_component_axes(
    poses, query_kind, reference_kind, in_place
):
    query, reference, base, n = poses
    before, reference_before = xyz(query).copy(), xyz(reference).copy()
    expected = before.copy()
    expected[[0, 2], :n] = base
    result = msm.structure.least_rmsd_align(
        query,
        selection=atom_selection(query, query_kind),
        structure_indices=[2, 0, 2],
        reference_molecular_system=reference,
        reference_selection=atom_selection(reference, reference_kind),
        reference_structure_index=1,
        use_gpu=False,
        in_place=in_place,
    )
    output = query if in_place else result
    assert (result is None) == in_place
    np.testing.assert_allclose(xyz(output), expected, rtol=0, atol=1e-11)
    np.testing.assert_array_equal(xyz(reference), reference_before)
    if not in_place:
        np.testing.assert_array_equal(xyz(query), before)


@pytest.mark.parametrize("precision,tolerance", [("double", 1e-11), ("single", 2e-6)])
@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
def test_cpu_precision_and_physical_units_are_delegated_to_fit(
    poses, precision, tolerance, unit
):
    query, reference, base, n = poses
    before = xyz(reference).copy()
    reference.structures.coordinates = puw.quantity(before * 10, "angstrom")
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = msm.structure.least_rmsd_align(
            query,
            reference_molecular_system=reference,
            reference_structure_index=1,
            precision=precision,
            use_gpu=False,
        )
    np.testing.assert_allclose(
        xyz(result)[:, :n], np.tile(base[None], (3, 1, 1)), rtol=0, atol=tolerance
    )
    np.testing.assert_allclose(xyz(reference), before, rtol=0, atol=1e-12)


@pytest.mark.parametrize("form", ["file:h5msm", "mdtraj.Trajectory"])
def test_reference_is_form_agnostic_and_read_only(poses, form, tmp_path):
    if form == "mdtraj.Trajectory":
        pytest.importorskip("mdtraj")
    query, reference, base, n = poses
    if form.startswith("file:"):
        reference = msm.convert(reference, to_form=str(tmp_path / "reference.h5msm"))
    else:
        reference = msm.convert(reference, to_form=form)
    before = xyz(reference).copy()
    result = msm.structure.least_rmsd_align(
        query,
        reference_molecular_system=reference,
        reference_structure_index=1,
        use_gpu=False,
    )
    # MDTraj stores float32 coordinates: compare with an independent SVD fit
    # to the actual quantized reference, not the pre-conversion float64 pose.
    query_xyz = xyz(query)
    query_atoms = msm.select(query, selection='atom_name=="CA"')
    reference_atoms = msm.select(reference, selection='atom_name=="CA"')
    right = np.asarray(before[1, reference_atoms], dtype=np.float64)
    expected = []
    for points in query_xyz:
        left = points[query_atoms]
        left_center, right_center = left.mean(axis=0), right.mean(axis=0)
        u, _, vh = np.linalg.svd((left - left_center).T @ (right - right_center))
        rotation = u @ np.diag([1.0, 1.0, np.linalg.det(u @ vh)]) @ vh
        expected.append((points[:n] - left_center) @ rotation + right_center)
    np.testing.assert_allclose(xyz(result)[:, :n], expected, rtol=0, atol=1e-10)
    np.testing.assert_array_equal(xyz(reference), before)


def test_matched_atom_names_remain_paired_after_reference_atom_permutation(poses):
    query, reference, base, n = poses
    reference = msm.permute_atoms(reference, atom_indices=list(range(n + 2, -1, -1)))
    before = xyz(reference).copy()
    result = msm.structure.least_rmsd_align(
        query,
        selection="backbone",
        reference_molecular_system=reference,
        reference_selection="backbone",
        reference_structure_index=1,
        use_gpu=False,
    )
    np.testing.assert_allclose(
        xyz(result)[:, :n], np.tile(base[None], (3, 1, 1)), rtol=0, atol=1e-11
    )
    np.testing.assert_array_equal(xyz(reference), before)


@pytest.mark.parametrize(
    "options",
    [
        {"selection": []},
        {"selection": [9999]},
        {"selection": [[0, 1], [2, 3]]},
        {"selection": [[0], [1, 2]]},
        {"selection": [True, False]},
        {"selection": [0.5]},
        {"selection": [-1]},
        {"reference_selection": []},
        {"reference_selection": [9999]},
        {"reference_selection": [True]},
        {"reference_selection": [0.5]},
        {"structure_indices": []},
        {"structure_indices": [-1]},
        {"structure_indices": [99]},
        {"reference_structure_index": 99},
        {"selection": [8, 18]},
        {"reference_selection": 'atom_name=="N"'},
    ],
)
def test_invalid_correspondences_reject_before_coordinate_edits(poses, options):
    query, reference, _, _ = poses
    before, reference_before = xyz(query).copy(), xyz(reference).copy()
    parameters = dict(
        reference_molecular_system=reference,
        reference_structure_index=1,
        use_gpu=False,
        in_place=True,
    )
    parameters.update(options)
    with pytest.raises((ArgumentError, StructuralInconsistencyError)):
        msm.structure.least_rmsd_align(query, **parameters)
    np.testing.assert_array_equal(xyz(query), before)
    np.testing.assert_array_equal(xyz(reference), reference_before)


def test_collinear_fit_rejects_before_publishing_coordinates(poses):
    query, reference, _, _ = poses
    anchors = msm.select(query, selection='atom_name=="CA"')
    before = xyz(query).copy()
    before[:, anchors] = np.column_stack(
        [np.arange(len(anchors)), np.zeros((len(anchors), 2))]
    )
    msm.set(query, coordinates=puw.quantity(before, "nm"))
    with pytest.raises(StructuralInconsistencyError):
        msm.structure.least_rmsd_align(
            query,
            reference_molecular_system=reference,
            reference_structure_index=1,
            use_gpu=False,
            in_place=True,
        )
    np.testing.assert_array_equal(xyz(query), before)


@pytest.mark.parametrize("in_place", [False, True])
def test_fitted_structures_invalidate_interactions_without_rebinding_old_views(
    poses, in_place
):
    query, reference, _, n = poses
    analysis = msm.Interactions.from_records(
        [
            dict(
                structure_index=i,
                interaction_type="hbond",
                participants=[
                    dict(role=role, atom_indices=[atom])
                    for role, atom in [("donor", 0), ("hydrogen", 1), ("acceptor", 2)]
                ],
                measurements={"distance": 0.2},
                evidence="synthetic",
            )
            for i in [0, 2]
        ],
        n_atoms=n + 3,
        n_structures=3,
        evaluated_structure_indices=[0, 1, 2],
        method="synthetic_fit_guard",
        measure_units={"distance": "nm"},
    )
    query.interactions = {"test": analysis}
    previous = query.interactions["test"]
    view = previous.query(structure_indices=[0])
    result = msm.structure.least_rmsd_align(
        query,
        structure_indices=[2, 0, 2],
        reference_molecular_system=reference,
        reference_structure_index=1,
        use_gpu=False,
        in_place=in_place,
    )
    output = query if in_place else result
    np.testing.assert_array_equal(
        output.interactions["test"].evaluated_structure_indices, [1]
    )
    assert previous.n_interactions == 2 and view.n_interactions == 1
    if not in_place:
        np.testing.assert_array_equal(
            query.interactions["test"].evaluated_structure_indices, [0, 1, 2]
        )


def test_sequence_gaps_preserve_original_group_and_atom_correspondence():
    query = msm.build.build_peptide("ACEALAGLYSERTHRNME")
    reference = msm.build.build_peptide("ACEALASERTHRNME")
    data = msm.get(
        query, element="atom", group_name=True, atom_name=True, output_type="dictionary"
    )
    ref_data = msm.get(
        reference,
        element="atom",
        group_name=True,
        atom_name=True,
        output_type="dictionary",
    )
    n = msm.get(query, n_atoms=True)
    i = np.arange(n, dtype=float)
    base = np.column_stack([i * 0.04, (i % 5) * 0.1, (i % 9) * 0.07])
    lookup = {
        (group, atom): point
        for group, atom, point in zip(
            data["group_name"], data["atom_name"], base, strict=True
        )
    }
    reference_base = np.array(
        [
            lookup[group, atom]
            for group, atom in zip(
                ref_data["group_name"], ref_data["atom_name"], strict=True
            )
        ]
    )
    msm.set(
        query, coordinates=puw.quantity(pose(base, 1, [1.0, -0.4, 0.7])[None], "nm")
    )
    msm.set(reference, coordinates=puw.quantity(reference_base[None], "nm"))
    before = xyz(query).copy()
    result = msm.structure.least_rmsd_align(
        query, reference_molecular_system=reference, use_gpu=False
    )
    np.testing.assert_allclose(xyz(result)[0], base, rtol=0, atol=1e-11)
    np.testing.assert_array_equal(xyz(query), before)
    # Caps and the unmatched GLY are not compact sequence positions.
    _, groups, reference_groups = msm.topology.get_sequence_identity(
        query, reference_molecular_system=reference
    )
    assert groups == [1, 3, 4] and reference_groups == [1, 2, 3]


@pytest.mark.parametrize(
    "case", ["balanced_missing_names", "duplicate_names", "no_sequence_matches"]
)
def test_ambiguous_or_empty_group_correspondences_reject_before_editing(poses, case):
    query, reference, _, _ = poses
    query_atoms = msm.select(query, selection='atom_name=="CA"')
    reference_atoms = msm.select(reference, selection='atom_name=="CA"')
    if case == "balanced_missing_names":
        query_atoms.append(
            msm.select(query, selection='group_index==1 and atom_name=="N"')[0]
        )
        reference_atoms.append(
            msm.select(reference, selection='group_index==3 and atom_name=="N"')[0]
        )
    elif case == "duplicate_names":
        extra = msm.select(query, selection='group_index==1 and atom_name=="N"')[0]
        msm.set(query, selection=[extra], atom_name=["CA"])
        query_atoms.append(extra)
    else:
        msm.set(
            query, element="group", selection=[1, 2, 3, 4, 5], group_name=["VAL"] * 5
        )
    before = xyz(query).copy()
    with pytest.raises(ArgumentError):
        msm.structure.least_rmsd_align(
            query,
            selection=query_atoms,
            reference_molecular_system=reference,
            reference_selection=reference_atoms,
            reference_structure_index=1,
            use_gpu=False,
            in_place=True,
        )
    np.testing.assert_array_equal(xyz(query), before)


def test_requested_external_syntax_is_resolved_before_sequence_projection(poses):
    pytest.importorskip("mdtraj")
    query, reference, base, n = poses
    result = msm.structure.least_rmsd_align(
        query,
        selection="name CA",
        reference_molecular_system=reference,
        reference_selection="name CA",
        reference_structure_index=1,
        syntax="MDTraj",
        use_gpu=False,
    )
    np.testing.assert_allclose(
        xyz(result)[:, :n], np.tile(base[None], (3, 1, 1)), rtol=0, atol=1e-11
    )
