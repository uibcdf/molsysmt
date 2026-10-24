"""Receive repaired observables and relation tools against independent geometry."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm

pytest.importorskip("molsysviewer.system_edits")
puw = msm.pyunitwizard
NEW = ("get_maximum_distances", "get_contacts", "get_rmsf")
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
    assert set(dir(view.addons.molsysmt.structure)) == set(NEW + OLD)
    assert not hasattr(view.addons.molsysmt.structure, "get_minimum_distances")
    assert not hasattr(view.addons.molsysmt.structure, "get_neighbors")
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
    if name == "get_maximum_distances":
        args.update(selection_2=[1, 3], pbc=False)
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
            getattr(empty.addons.molsysmt.structure, name)()


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
