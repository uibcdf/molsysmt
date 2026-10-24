"""Receive repaired observables and relation tools against independent geometry."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm

pytest.importorskip("molsysviewer.system_edits")
puw = msm.pyunitwizard
NEW = (
    "get_maximum_distances",
    "get_contacts",
    "get_rmsf",
    "get_minimum_distances",
    "get_neighbors",
)
OLD = (
    "get_distances",
    "get_vectors",
    "get_center",
    "get_radius_of_gyration",
    "get_angles",
    "get_dihedral_angles",
    "get_rmsd",
    "get_least_rmsd",
    "get_principal_axes",
    "get_least_squares_plane",
)
SCOPE = [2, 0, 2]


def same(actual, expected):
    assert type(actual) is type(expected)
    if puw.is_quantity(actual):
        assert puw.get_unit(actual) == puw.get_unit(expected)
        np.testing.assert_allclose(
            puw.get_value(actual), puw.get_value(expected), equal_nan=True
        )
    elif isinstance(actual, dict):
        assert actual.keys() == expected.keys()
        for k in actual:
            same(actual[k], expected[k])
    elif isinstance(actual, (list, tuple)):
        assert len(actual) == len(expected)
        for a, b in zip(actual, expected):
            same(a, b)
    elif isinstance(actual, np.ndarray):
        assert actual.dtype == expected.dtype
        np.testing.assert_equal(actual, expected)
    else:
        assert actual == expected


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as result:
            a = msm.Interactions.from_records(
                [],
                n_atoms=result.molsys.get_n_atoms(),
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.native.repairs",
            )
            result.interactions.attach(a, name="preserve", assume_aligned=True)
            yield result


def coordinates(view, atoms="all", structures=SCOPE):
    return puw.get_value(
        msm.get(
            view.molsys,
            element="atom",
            selection=atoms,
            structure_indices=structures,
            coordinates=True,
        ),
        to_unit="nm",
    )


@pytest.mark.parametrize("name", NEW)
def test_native_signatures_explicit_namespace_and_validation(view, name):
    signature = inspect.signature(getattr(msm.structure, name))
    expected = list(signature.parameters.values())[1:]
    if name == "get_maximum_distances":
        expected.append(
            inspect.Parameter(
                "skip_digestion", inspect.Parameter.KEYWORD_ONLY, default=False
            )
        )
    method = getattr(view.addons.molsysmt.structure, name)
    assert list(inspect.signature(method).parameters.values()) == expected
    assert method.digestion_plan is not None
    assert "current view.molsys" in inspect.getdoc(method)
    assert "not a scene object" in inspect.getdoc(method)
    # The analyses receiving file guards the complete expanded namespace.
    assert set(NEW + OLD) <= set(dir(view.addons.molsysmt.structure))
    assert not hasattr(view.addons.molsysmt, name)


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
def test_repaired_heavy_distances_preserve_both_populations_and_structure_axes(
    view, unit
):
    a, b = [4, 0, 2], [5, 3]
    other = [0, 2, 0]
    xyz = coordinates(view, a, SCOPE)
    ref = coordinates(view, b, other)
    expected = np.linalg.norm(xyz[:, :, None] - ref[:, None], axis=-1)
    args = dict(
        selection=a,
        selection_2=b,
        structure_indices=SCOPE,
        structure_indices_2=other,
        pbc=False,
        heavy_mode="force",
        output_indices="atom",
        output_structure_indices="structure",
    )
    with puw.context(standard_units=[unit, "ps", "radians"]):
        with msm.configure.context(chunk_size=1, chunk_memory_fraction=None):
            actual = view.addons.molsysmt.structure.get_distances(**args)
            same(actual, msm.structure.get_distances(view.molsys, **args))
        assert puw.get_unit(actual[-1]) == puw.unit(unit)
    assert actual[-1].shape == (3, 3, 2)
    np.testing.assert_array_equal(actual[0], a)
    np.testing.assert_array_equal(actual[1], b)
    np.testing.assert_array_equal(actual[2], SCOPE)
    np.testing.assert_array_equal(actual[3], other)
    np.testing.assert_allclose(
        puw.get_value(actual[-1], to_unit="nm"), expected, atol=1e-12
    )


@pytest.mark.parametrize("name", ["get_radius_of_gyration", "get_rmsf"])
@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("mode", ["off", "force"])
def test_repaired_observable_units_match_independent_values_across_blocks(
    view, name, unit, mode
):
    atoms = [4, 0, 2]
    xyz = coordinates(view, atoms)
    args = dict(selection=atoms, structure_indices=SCOPE, heavy_mode=mode)
    if name == "get_radius_of_gyration":
        weights = np.array([1.0, 3.0, 2.0])
        args["weights"] = weights
        center = np.average(xyz, axis=1, weights=weights)
        expected = np.sqrt(
            np.average(
                np.sum((xyz - center[:, None]) ** 2, axis=-1), axis=1, weights=weights
            )
        )
    else:
        expected = np.sqrt(
            np.mean(np.sum((xyz - xyz.mean(axis=0)) ** 2, axis=-1), axis=0)
        )
    with puw.context(standard_units=[unit, "ps", "radians"]):
        policy = dict(puw.configure.get_standard_units())
        with msm.configure.context(chunk_size=1, chunk_memory_fraction=None):
            actual = getattr(view.addons.molsysmt.structure, name)(**args)
            same(actual, getattr(msm.structure, name)(view.molsys, **args))
        assert puw.get_unit(actual) == puw.unit(unit)
        assert dict(puw.configure.get_standard_units()) == policy
    np.testing.assert_allclose(
        puw.get_value(actual, to_unit="nm"), expected, atol=1e-12
    )


@pytest.mark.parametrize("skip", [False, True])
def test_repaired_sequence_identity_keeps_source_groups_and_native_flag(view, skip):
    pytest.importorskip("Bio")
    native = inspect.signature(msm.topology.get_sequence_identity)
    bound = view.addons.molsysmt.topology.get_sequence_identity
    assert (
        list(inspect.signature(bound).parameters.values())
        == list(native.parameters.values())[1:]
    )
    assert bound(reference_molecular_system=view.molsys, skip_digestion=skip) == (
        100.0,
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
    )


@pytest.mark.parametrize("entity", [(True, True), (False, True), (True, False)])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_maximum_values_and_local_endpoint_positions_match_numpy(view, entity, unit):
    a, b = [25, 10, 0], [0, 25]
    matrix = np.linalg.norm(
        coordinates(view, a)[:, :, None] - coordinates(view, b)[:, None], axis=-1
    )
    if entity == (True, True):
        indices = np.array([np.unravel_index(x.argmax(), x.shape) for x in matrix])
        values = matrix.max(axis=(1, 2))
    elif entity == (False, True):
        indices = matrix.argmax(axis=2)
        values = matrix.max(axis=2)
    else:
        indices = matrix.argmax(axis=1)
        values = matrix.max(axis=1)
    args = dict(
        selection=a,
        selection_2=b,
        structure_indices=SCOPE,
        pbc=False,
        as_entity=entity[0],
        as_entity_2=entity[1],
    )
    with puw.context(standard_units=[unit, "ps", "radians"]):
        actual = view.addons.molsysmt.structure.get_maximum_distances(
            **args, skip_digestion=True
        )
        same(actual, msm.structure.get_maximum_distances(view.molsys, **args))
    np.testing.assert_array_equal(actual[0], indices)
    np.testing.assert_allclose(
        puw.get_value(actual[1], to_unit="nm"), values, atol=1e-12
    )


def test_maximum_has_independent_second_system_weights_and_explicit_pairs(view):
    reference = msm.copy(view.molsys)
    msm.set(
        reference,
        coordinates=msm.get(reference, element="atom", coordinates=True)
        + puw.quantity([1.0, 0.0, 0.0], "nm"),
    )
    args = dict(
        selection=[0, 2],
        selection_2=[10, 25],
        structure_indices=SCOPE,
    )
    args.update(
        molecular_system_2=reference,
        structure_indices_2=[0, 2, 0],
        center_of_atoms=True,
        center_of_atoms_2=True,
        weights=[1.0, 1.0],
        weights_2=[1.0, 3.0],
        pbc=False,
    )
    a = np.average(coordinates(view, [0, 2]), axis=1, weights=[1.0, 1.0])
    b = puw.get_value(
        msm.get(
            reference,
            element="atom",
            selection=[10, 25],
            structure_indices=[0, 2, 0],
            coordinates=True,
        ),
        to_unit="nm",
    )
    expected = np.linalg.norm(a - np.average(b, axis=1, weights=[1.0, 3.0]), axis=-1)
    actual = view.addons.molsysmt.structure.get_maximum_distances(**args)
    same(actual, msm.structure.get_maximum_distances(view.molsys, **args))
    np.testing.assert_allclose(
        puw.get_value(actual[1], to_unit="nm"), expected, atol=1e-12
    )
    args = dict(
        selection=[0, 2, 4],
        selection_2=[1, 3, 5],
        structure_indices=SCOPE,
        pairs=True,
        pbc=False,
    )
    matrix = np.linalg.norm(
        coordinates(view, [0, 2, 4]) - coordinates(view, [1, 3, 5]), axis=-1
    )
    actual = view.addons.molsysmt.structure.get_maximum_distances(**args)
    np.testing.assert_array_equal(actual[0], matrix.argmax(axis=1))
    np.testing.assert_allclose(
        puw.get_value(actual[1], to_unit="nm"), matrix.max(axis=1), atol=1e-12
    )


@pytest.mark.parametrize("cell_list", [False, True])
@pytest.mark.parametrize("pairs", [False, True])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_contacts_maps_match_independent_threshold_and_native_routes(
    view, cell_list, pairs, unit
):
    a, b = [0, 10, 25], [1, 14, 27]
    xyz, ref = coordinates(view, a), coordinates(view, b)
    delta = xyz - ref if pairs else xyz[:, :, None] - ref[:, None]
    expected = np.linalg.norm(delta, axis=-1) <= 0.6
    args = dict(
        selection=a,
        selection_2=b,
        structure_indices=SCOPE,
        threshold=puw.quantity(0.6, "nm"),
        pbc=False,
        pairs=pairs,
        cell_list=cell_list,
        use_gpu=False,
    )
    with puw.context(standard_units=[unit, "ps", "radians"]):
        actual = view.addons.molsysmt.structure.get_contacts(**args)
        same(actual, msm.structure.get_contacts(view.molsys, **args))
    assert actual.dtype == np.bool_
    np.testing.assert_array_equal(actual, expected)


@pytest.mark.parametrize("output", ["pairs", "sorted pairs"])
@pytest.mark.parametrize("indices", ["selection", "atom"])
def test_contact_pair_outputs_preserve_native_source_mapping(view, output, indices):
    args = dict(
        selection=[25, 0, 10],
        selection_2=[40, 55],
        structure_indices=SCOPE,
        threshold="100 nm",
        pbc=False,
        output_type=output,
        output_indices=indices,
        cell_list=False,
        use_gpu=False,
    )
    actual = view.addons.molsysmt.structure.get_contacts(**args)
    same(actual, msm.structure.get_contacts(view.molsys, **args))
    assert len(actual) == 3
    expected = (
        [[i, j] for i in range(3) for j in range(2)]
        if indices == "selection"
        else [[i, j] for i in [25, 0, 10] for j in [40, 55]]
    )
    if output == "sorted pairs":
        expected = sorted(expected)
    for frame in actual:
        assert frame == expected


@pytest.mark.parametrize(
    "name,args",
    [
        (
            "get_maximum_distances",
            dict(selection=[0, 1], as_entity=False, as_entity_2=False, pbc=False),
        ),
        ("get_contacts", dict(selection=[0, 1], threshold="1 ps", use_gpu=False)),
        ("get_rmsf", dict(selection=[])),
        ("get_rmsf", dict(structure_indices=[])),
    ],
)
def test_native_errors_leave_scene_sync_and_named_analysis_untouched(view, name, args):
    state = view.export_state()
    status = view.addons.molsysmt.get_sync_status()
    analysis = view.molsys.interactions["preserve"]
    with pytest.raises(Exception) as error:
        getattr(msm.structure, name)(view.molsys, **args)
    with pytest.raises(type(error.value)):
        getattr(view.addons.molsysmt.structure, name)(**args)
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )
    assert view.molsys.interactions["preserve"] is analysis


@pytest.mark.parametrize("name", NEW)
def test_lifetime_primary_override_and_input_preservation(view, name):
    args = dict(selection=[0, 2, 4], structure_indices=SCOPE)
    if name == "get_contacts":
        args.update(threshold="0 nm", selection_2=[1, 3], pbc=False, use_gpu=False)
    if name in {"get_maximum_distances", "get_minimum_distances"}:
        args.update(selection_2=[1, 3], pbc=False)
    if name == "get_neighbors":
        args.update(selection_2=[1, 3], n_neighbors=1, pbc=False)
    old = coordinates(view).copy()
    state = view.export_state()
    analysis = view.molsys.interactions["preserve"]
    bound = getattr(view.addons.molsysmt.structure, name)
    bound(**args)
    np.testing.assert_array_equal(coordinates(view), old)
    assert (
        view.export_state() == state
        and view.molsys.interactions["preserve"] is analysis
    )
    with pytest.raises(TypeError):
        bound(**args, molecular_system=object(), skip_digestion=True)
    with pytest.raises(Exception):
        bound(**args, skip_digestion="yes")
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        bound(**args, skip_digestion=True)
    with msv.MolSysView() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty_args = {"n_neighbors": 1} if name == "get_neighbors" else {}
            getattr(empty.addons.molsysmt.structure, name)(**empty_args)


def test_cached_rmsf_reads_pending_data_then_follows_replacement(view):
    bound = view.addons.molsysmt.structure.get_rmsf
    xyz = msm.get(view.molsys, element="atom", structure_indices=[2], coordinates=True)
    view.addons.molsysmt.basic.set(
        structure_indices=[2],
        coordinates=xyz + puw.quantity(0.2, "nm"),
        update_view=False,
    )
    status = view.addons.molsysmt.get_sync_status()
    assert status["state"] == "pending"
    same(bound(), msm.structure.get_rmsf(view.molsys))
    assert view.addons.molsysmt.get_sync_status() == status
    view.addons.molsysmt.sync_view()
    with msv.demo["dialanine"] as replacement:
        view.load(replacement.molsys, mode="replace")
    same(bound(), msm.structure.get_rmsf(view.molsys))


@pytest.mark.parametrize("entity", [(True, True), (False, True), (True, False)])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_minimum_indices_and_values_match_independent_geometry(view, entity, unit):
    first, second = [25, 10, 0], [0, 25]
    matrix = np.linalg.norm(
        coordinates(view, first)[:, :, None] - coordinates(view, second)[:, None],
        axis=-1,
    )
    if entity == (True, True):
        indices = np.array([np.unravel_index(x.argmin(), x.shape) for x in matrix])
        values = matrix.min(axis=(1, 2))
    else:
        axis = 2 if entity == (False, True) else 1
        indices, values = matrix.argmin(axis=axis), matrix.min(axis=axis)
    args = dict(
        selection=first,
        selection_2=second,
        structure_indices=SCOPE,
        as_entity=entity[0],
        as_entity_2=entity[1],
        pbc=False,
    )
    with puw.context(standard_units=[unit, "ps", "radians"]):
        actual = view.addons.molsysmt.structure.get_minimum_distances(**args)
        same(actual, msm.structure.get_minimum_distances(view.molsys, **args))
        assert puw.get_unit(actual[1]) == puw.unit(unit)
    np.testing.assert_array_equal(actual[0], indices)
    np.testing.assert_allclose(puw.get_value(actual[1], to_unit="nm"), values)


@pytest.mark.parametrize("name", ["get_minimum_distances", "get_neighbors"])
@pytest.mark.parametrize("two_sources", [False, True])
@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
def test_repaired_bound_endpoints_keep_independent_weights(
    view, name, two_sources, unit
):
    reference = msm.copy(view.molsys)
    msm.set(
        reference,
        coordinates=msm.get(reference, element="atom", coordinates=True)
        + puw.quantity([10.0, 0.0, 0.0], "nm"),
    )
    second = reference if two_sources else view.molsys
    first_atoms, second_atoms, second_structures = [0, 2], [10, 25, 4], [0, 2, 0]
    weights, weights_2 = np.array([1.0, 1.0]), np.array([1.0, 3.0, 2.0])
    other_xyz = puw.get_value(
        msm.get(
            second,
            element="atom",
            selection=second_atoms,
            structure_indices=second_structures,
            coordinates=True,
        ),
        to_unit="nm",
    )
    expected = np.linalg.norm(
        np.average(coordinates(view, first_atoms), axis=1, weights=weights)
        - np.average(other_xyz, axis=1, weights=weights_2),
        axis=-1,
    )
    args = dict(
        selection=first_atoms,
        selection_2=second_atoms,
        molecular_system_2=reference if two_sources else None,
        structure_indices=SCOPE,
        structure_indices_2=second_structures,
        center_of_atoms=True,
        center_of_atoms_2=True,
        weights=weights,
        weights_2=weights_2,
        pbc=False,
    )
    if name == "get_neighbors":
        args["n_neighbors"] = 1
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    before, other_before = coordinates(view).copy(), other_xyz.copy()
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = getattr(view.addons.molsysmt.structure, name)(
            **args, skip_digestion=True
        )
        same(result, getattr(msm.structure, name)(view.molsys, **args))
        assert puw.get_unit(result[1]) == puw.unit(unit)
    np.testing.assert_allclose(
        puw.get_value(result[1], to_unit="nm").reshape(-1), expected
    )
    np.testing.assert_array_equal(weights, [1.0, 1.0])
    np.testing.assert_array_equal(weights_2, [1.0, 3.0, 2.0])
    np.testing.assert_array_equal(coordinates(view), before)
    np.testing.assert_array_equal(
        puw.get_value(
            msm.get(
                second,
                element="atom",
                selection=second_atoms,
                structure_indices=second_structures,
                coordinates=True,
            ),
            to_unit="nm",
        ),
        other_before,
    )
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )


@pytest.mark.parametrize("kind", ["count", "threshold"])
@pytest.mark.parametrize("implicit_selection", [False, True])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_bound_neighbors_use_translated_reference_and_independent_structures(
    view, kind, implicit_selection, unit
):
    reference = msm.copy(view.molsys)
    msm.set(
        reference,
        coordinates=msm.get(reference, element="atom", coordinates=True)
        + puw.quantity([10.0, 0.0, 0.0], "nm"),
    )
    first = [25, 0, 10]
    second = first if implicit_selection else [4, 2]
    ref = puw.get_value(
        msm.get(
            reference,
            element="atom",
            selection=second,
            structure_indices=[0, 2, 0],
            coordinates=True,
        ),
        to_unit="nm",
    )
    matrix = np.linalg.norm(
        coordinates(view, first)[:, :, None] - ref[:, None], axis=-1
    )
    args = dict(
        selection=first,
        selection_2=None if implicit_selection else second,
        structure_indices=SCOPE,
        structure_indices_2=[0, 2, 0],
        molecular_system_2=reference,
        pbc=False,
    )
    args.update(n_neighbors=1) if kind == "count" else args.update(threshold="10 nm")
    with puw.context(standard_units=[unit, "ps", "radians"]):
        actual = view.addons.molsysmt.structure.get_neighbors(**args)
        native = msm.structure.get_neighbors(view.molsys, **args)
        assert puw.get_unit(actual[1]) == puw.unit(unit)
    for s in range(3):
        for i in range(3):
            expected = np.argsort(matrix[s, i], kind="stable")
            expected = (
                expected[:1]
                if kind == "count"
                else expected[matrix[s, i, expected] <= 10]
            )
            np.testing.assert_array_equal(actual[0][s, i], expected)
            np.testing.assert_array_equal(actual[0][s, i], native[0][s, i])
            np.testing.assert_allclose(
                puw.get_value(actual[1][s, i], to_unit="nm"), matrix[s, i, expected]
            )


def test_bound_minimum_pair_indices_are_local_and_native(view):
    first, second = [0, 2, 4], [1, 3, 5]
    values = np.linalg.norm(
        coordinates(view, first) - coordinates(view, second), axis=-1
    )
    actual = view.addons.molsysmt.structure.get_minimum_distances(
        selection=first,
        selection_2=second,
        structure_indices=SCOPE,
        pairs=True,
        pbc=False,
    )
    np.testing.assert_array_equal(actual[0], values.argmin(axis=1))
    np.testing.assert_allclose(
        puw.get_value(actual[1], to_unit="nm"), values.min(axis=1)
    )


@pytest.mark.parametrize("kind", ["csr", "pairs"])
def test_bound_neighbor_sparse_outputs_keep_native_atom_identity(view, kind):
    first, second = [25, 0, 10], [4, 2]
    matrix = np.linalg.norm(
        coordinates(view, first)[:, :, None] - coordinates(view, second)[:, None],
        axis=-1,
    )
    args = dict(
        selection=first,
        selection_2=second,
        structure_indices=SCOPE,
        threshold="0.6 nm",
        output_type=kind,
        pbc=False,
    )
    if kind == "pairs":
        args["output_indices"] = "atom"
    result = view.addons.molsysmt.structure.get_neighbors(**args)
    same(result, msm.structure.get_neighbors(view.molsys, **args))
    for s in range(3):
        expected_pairs, expected_values = [], []
        for i in range(3):
            expected = np.argsort(matrix[s, i], kind="stable")
            expected = expected[matrix[s, i, expected] <= 0.6]
            if kind == "csr":
                lo, hi = result[0][s * 3 + i : s * 3 + i + 2]
                np.testing.assert_array_equal(result[1][lo:hi], expected)
                np.testing.assert_allclose(
                    puw.get_value(result[2][lo:hi], to_unit="nm"),
                    matrix[s, i, expected],
                )
            else:
                expected_pairs.extend([[first[i], second[j]] for j in expected])
                expected_values.extend(matrix[s, i, expected])
        if kind == "pairs":
            order = sorted(range(len(expected_pairs)), key=lambda i: expected_pairs[i])
            assert result[0][s] == [expected_pairs[i] for i in order]
            if order:
                np.testing.assert_allclose(
                    puw.get_value(result[1][s], to_unit="nm"),
                    np.asarray(expected_values)[order],
                )
            else:
                assert len(result[1][s]) == 0


@pytest.mark.parametrize(
    "name,args",
    [
        (
            "get_minimum_distances",
            dict(selection=[0, 1], as_entity=False, as_entity_2=False),
        ),
        ("get_minimum_distances", dict(selection=[], selection_2=[1])),
        ("get_neighbors", dict(selection=[0, 1])),
        ("get_neighbors", dict(selection=[0, 1], threshold=None, n_neighbors=1)),
        ("get_neighbors", dict(selection=[0, 1], threshold="1 nm", n_neighbors=1)),
        ("get_neighbors", dict(selection=[0, 1], n_neighbors=3)),
        ("get_neighbors", dict(selection=[0, 1], n_neighbors=1, pairs=True)),
    ],
)
def test_bound_distance_family_errors_preserve_view_and_analysis(view, name, args):
    args["pbc"] = False
    test_native_errors_leave_scene_sync_and_named_analysis_untouched(view, name, args)


@pytest.mark.parametrize("name", ["get_minimum_distances", "get_neighbors"])
def test_cached_relation_reader_follows_pending_science_and_view_replacement(
    view, name
):
    method = getattr(view.addons.molsysmt.structure, name)
    args = dict(selection=[0, 2], selection_2=[1, 3], pbc=False)
    if name == "get_neighbors":
        args["n_neighbors"] = 1
    xyz = msm.get(view.molsys, element="atom", selection=[0, 2], coordinates=True)
    view.addons.molsysmt.basic.set(
        selection=[0, 2], coordinates=xyz + puw.quantity(0.2, "nm"), update_view=False
    )
    status = view.addons.molsysmt.get_sync_status()
    assert status["state"] == "pending"
    same(method(**args), getattr(msm.structure, name)(view.molsys, **args))
    assert view.addons.molsysmt.get_sync_status() == status
    view.addons.molsysmt.sync_view()
    with msv.demo["dialanine"] as replacement:
        view.load(replacement.molsys, mode="replace")
    same(method(**args), getattr(msm.structure, name)(view.molsys, **args))
