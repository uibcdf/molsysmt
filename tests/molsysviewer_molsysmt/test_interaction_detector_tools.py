"""Receive raw native detections independently from saved analyses and rendering."""

import inspect
from collections.abc import Mapping
from copy import deepcopy

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError
from molsysviewer.system_edits import SystemEditPendingError
from rdkit import Chem

import molsysmt as msm

puw = msm.pyunitwizard
LEGACY = ("get_buch_hbonds", "get_luzard_chandler_hbonds")
HBONDS = LEGACY + ("get_hbonds",)
NAMES = HBONDS + ("get_disulfide_candidates",)
RECOGNITION = (
    "get_donor_atoms",
    "get_acceptor_atoms",
    "get_hbond_sites",
    "get_hbond_site_directions",
)


def hbond_system(periodic=False):
    molecule = Chem.AddHs(Chem.MolFromSmiles("O.O"))
    xyz = np.array(
        [
            [0, 0, 0],
            [0.28, 0, 0],
            [0.1, 0, 0],
            [0, 0.1, 0],
            [0.28, 0.1, 0],
            [0.28, 0, 0.1],
        ]
    )
    if periodic:
        xyz += [0.86, 0, 0]
        xyz[[1, 4, 5], 0] -= 1
    coordinates = np.repeat(xyz[None], 3, axis=0)
    coordinates[1, [1, 4, 5]] += [0, 0.4, 0]
    if not periodic:
        coordinates[2, [1, 4, 5]] += [0.01, 0, 0]
    source = msm.convert(molecule)
    source.structures.append(
        coordinates=puw.quantity(coordinates, "nm"),
        box=puw.quantity(np.repeat(np.eye(3)[None], 3, axis=0), "nm")
        if periodic
        else None,
    )
    return source


def sulfur_system(periodic=False, with_bond=False):
    builder = msm.MolSysBuilder()
    for group in ["CYS", "CYS", "MET"]:
        atom = builder.add_atom(
            atom_name="SG" if group == "CYS" else "SD", atom_type="S"
        )
        builder.add_group([atom], group_name=group)
    if with_bond:
        builder.add_bond(0, 1)
    xyz = np.array(
        [
            [[0, 0, 0], [0.20, 0, 0], [0.1, 0, 0]],
            [[0, 0, 0], [0.35, 0, 0], [0.1, 0, 0]],
            [[0, 0, 0], [0.19, 0, 0], [0.1, 0, 0]],
        ]
    )
    if periodic:
        xyz[:, 0, 0] = 0.9
        xyz[:, 1, 0] = [0.1, 0.25, 0.09]
        builder.set_box(puw.quantity(np.repeat(np.eye(3)[None], 3, axis=0), "nm"))
    builder.set_coordinates(puw.quantity(xyz, "nm"))
    return builder.build()


def target(view, name):
    return (
        view.addons.molsysmt.interactions.disulfides
        if name == "get_disulfide_candidates"
        else view.addons.molsysmt.interactions.hbonds
    )


def native(name):
    return getattr(
        msm.interactions.disulfides
        if name == "get_disulfide_candidates"
        else msm.interactions.hbonds,
        name,
    )


def same(actual, expected):
    if isinstance(expected, msm.Interactions):
        same(actual.to_dict(), expected.to_dict())
    elif isinstance(expected, Mapping):
        assert actual.keys() == expected.keys()
        for key in expected:
            same(actual[key], expected[key])
    elif puw.is_quantity(expected):
        assert puw.get_unit(actual) == puw.get_unit(expected)
        np.testing.assert_array_equal(puw.get_value(actual), puw.get_value(expected))
    elif isinstance(expected, (list, tuple)):
        assert type(actual) is type(expected) and len(actual) == len(expected)
        for first, second in zip(actual, expected):
            same(first, second)
    else:
        np.testing.assert_equal(actual, expected)


@pytest.fixture
def view(request):
    source = (
        sulfur_system()
        if request.param == "get_disulfide_candidates"
        else hbond_system()
    )
    with msv.new_view(source) as result:
        result.regions.add(selection=[0], tag="source")
        result.interactions.attach(
            msm.Interactions.from_records(
                [],
                n_atoms=source.get_n_atoms(),
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.detectors",
            ),
            name="preserve",
            assume_aligned=True,
        )
        yield result


@pytest.mark.parametrize("view", NAMES, indirect=True)
def test_explicit_signature_native_defaults_and_family_navigation(view, request):
    name = request.node.callspec.params["view"]
    method = getattr(target(view, name), name)
    signature = inspect.signature(native(name))
    assert inspect.signature(method) == signature.replace(
        parameters=list(signature.parameters.values())[1:]
    )
    assert method.digestion_plan is not None
    assert set(dir(view.addons.molsysmt.interactions)) == {
        "hbonds",
        "disulfides",
        "ionic",
        "hydrophobic",
        "halogen_bonds",
    }
    assert set(dir(view.addons.molsysmt.interactions.hbonds)) == set(
        RECOGNITION + HBONDS
    )
    assert dir(view.addons.molsysmt.interactions.disulfides) == [
        "get_disulfide_candidates"
    ]
    assert not hasattr(view.addons.molsysmt, name)
    assert not hasattr(view.addons.molsysmt.interactions, "metal_coordination")
    assert "not a scene object" in inspect.getdoc(method)
    assert "These tools do not detect interaction occurrences" not in inspect.getdoc(
        method
    )
    for kwargs in [
        dict(update_view=False),
        dict(molecular_system=view.molsys),
        dict(prepare=True),
    ]:
        with pytest.raises(UnknownArgumentError):
            method(**kwargs)
    result = method(pbc=False)
    assert (
        isinstance(result, msm.Interactions)
        if name == "get_hbonds"
        else isinstance(result, tuple)
    )


@pytest.mark.parametrize("view", NAMES, indirect=True)
@pytest.mark.parametrize("skip", [False, True])
def test_sparse_native_result_and_source_scene_ownership(view, request, skip):
    name = request.node.callspec.params["view"]
    source = view.molsys
    before = view.export_state()
    core = view.interactions
    atoms = source.topology.atoms.copy(deep=True)
    bonds = source.chemical_states._states[0].bonds.copy(deep=True)
    xyz = puw.get_value(source.structures.coordinates).copy()
    preserved = source.interactions["preserve"]
    coverage = deepcopy(preserved.to_dict())
    args = dict(
        structure_indices=[2, 1, 0, 2],
        pbc=False,
        output_type="molsysmt.interactions",
        skip_digestion=skip,
    )
    if name == "get_buch_hbonds":
        args["distance_threshold"] = puw.quantity(0.23, "nm")
    if name == "get_luzard_chandler_hbonds":
        args.update(
            distance_threshold=puw.quantity(0.35, "nm"),
            angle_threshold=puw.quantity(np.pi / 6, "radians"),
        )
    result = getattr(target(view, name), name)(**args)
    same(result, native(name)(source, **args))
    assert isinstance(result, msm.Interactions) and result.n_interactions == 2
    assert set(result.evaluated_structure_indices) == {0, 1, 2}
    assert result.query(structure_indices=[1]).n_interactions == 0
    assert view.interactions is core and source is view.molsys
    assert (
        set(source.interactions) == {"preserve"}
        and source.interactions["preserve"] is preserved
    )
    same(preserved.to_dict(), coverage)
    pd.testing.assert_frame_equal(source.topology.atoms, atoms)
    pd.testing.assert_frame_equal(source.chemical_states._states[0].bonds, bonds)
    np.testing.assert_array_equal(puw.get_value(source.structures.coordinates), xyz)
    assert view.export_state() == before
    # A detached analysis remains usable after its view closes.
    view.close()
    assert result.query().n_interactions == 2


@pytest.mark.parametrize("view", LEGACY + ("get_disulfide_candidates",), indirect=True)
def test_tuple_order_repetition_ragged_empties_and_units(view, request):
    name = request.node.callspec.params["view"]
    method = getattr(target(view, name), name)
    with puw.context(standard_units=["angstrom", "degrees", "ps", "e"]):
        result = method(structure_indices=[2, 1, 0, 2], pbc=False)
    assert isinstance(result[0], list)
    assert [len(row) for row in result[0]] == [1, 0, 1, 1]
    expected_pair = [0, 1] if name == "get_disulfide_candidates" else [0, 2, 1]
    assert result[0][0].tolist() == [expected_pair]
    expected = (
        [0.19, None, 0.20, 0.19]
        if name == "get_disulfide_candidates"
        else (
            [0.29, None, 0.28, 0.29]
            if name == "get_luzard_chandler_hbonds"
            else [0.19, None, 0.18, 0.19]
        )
    )
    for observed, value in zip(result[1], expected):
        assert puw.get_unit(observed) == puw.unit("nm")
        if value is None:
            assert observed.shape == (0,)
        else:
            np.testing.assert_allclose(puw.get_value(observed, to_unit="nm"), [value])
    if name == "get_luzard_chandler_hbonds":
        for angle in result[2]:
            assert puw.get_unit(angle) == puw.unit("radians")
            np.testing.assert_allclose(puw.get_value(angle), 0)
    empty = method(structure_indices=[1], pbc=False)
    assert empty[0][0].shape == (0, 2 if name == "get_disulfide_candidates" else 3)
    assert empty[0][0].dtype == np.int64


@pytest.mark.parametrize("view", NAMES, indirect=True)
def test_evaluated_empty_vs_unevaluated_and_independent_measure_values(view, request):
    name = request.node.callspec.params["view"]
    method = getattr(target(view, name), name)
    result = method(
        structure_indices=[2, 0, 2], pbc=False, output_type="molsysmt.Interactions"
    )
    assert set(result.evaluated_structure_indices) == {0, 2}
    assert 1 not in result.evaluated_structure_indices
    assert result.n_interactions == 2 and result.n_structures == 3
    for frame, distance in [
        (
            0,
            0.20
            if name == "get_disulfide_candidates"
            else (0.28 if name == "get_luzard_chandler_hbonds" else 0.18),
        ),
        (
            2,
            0.19
            if name == "get_disulfide_candidates"
            else (0.29 if name == "get_luzard_chandler_hbonds" else 0.19),
        ),
    ]:
        observed = result.query(structure_indices=[frame]).to_dict()
        key = "hydrogen_acceptor_distance" if name == "get_hbonds" else "distance"
        np.testing.assert_allclose(observed["measurements"][key], [distance])
        assert result.measure_units[key] == "nm"
    refs = result.query().to_dict()["occurrence_indices"]
    assert refs.dtype == np.int64 and len(np.unique(refs)) == 2
    empty = method(
        structure_indices=[1], pbc=False, output_type="molsysmt.Interactions"
    )
    assert empty.n_interactions == 0 and empty.evaluated_structure_indices.tolist() == [
        1
    ]
    assert empty.method and empty.software["molsysmt"]
    assert empty.parameters["attribution"]["items"]


@pytest.mark.parametrize(
    "method",
    ["baker_hubbard", "wernet_nilsson", "cpptraj", "prolif", "mdanalysis_geometry"],
)
@pytest.mark.parametrize(
    "mode,selection,second,count",
    [
        ("internal", [0, 2, 1], None, 2),
        ("internal", [0, 2], None, 0),
        ("incident", [2], None, 2),
        ("between", [0, 2], [1], 2),
    ],
)
def test_modern_profiles_and_scopes_keep_explicit_sites_and_roles(
    method, mode, selection, second, count
):
    with msv.new_view(hbond_system()) as view:
        args = dict(
            method=method,
            selection_mode=mode,
            selection=selection,
            selection_2=second,
            structure_indices=[2, 0, 2],
            pbc=False,
        )
        if method == "mdanalysis_geometry":
            args.update(
                donor_hydrogen_pairs=np.array([[0, 2]], dtype=np.int64),
                acceptor_atom_indices=np.array([1], dtype=np.int64),
            )
        result = view.addons.molsysmt.interactions.hbonds.get_hbonds(**args)
        same(result, msm.interactions.hbonds.get_hbonds(view.molsys, **args))
        assert result.n_interactions == count
        assert result.evaluated_structure_indices.tolist() == [0, 2]
        if count:
            assert result.participant_roles == ("donor", "hydrogen", "acceptor")
            assert result.participant_atoms.tolist() == [0, 2, 1]
            np.testing.assert_allclose(result.measurements["dha_angle"], np.pi)
            assert result.measure_units["dha_angle"] == "radians"
        if method == "mdanalysis_geometry":
            np.testing.assert_array_equal(args["donor_hydrogen_pairs"], [[0, 2]])
            np.testing.assert_array_equal(args["acceptor_atom_indices"], [1])


def test_modern_typed_dictionary_execution_and_external_syntax():
    with msv.new_view(hbond_system()) as view:
        method = view.addons.molsysmt.interactions.hbonds.get_hbonds
        args = dict(
            selection="index 0 1 2",
            syntax="MDTraj",
            structure_indices=[2, 0],
            pbc=False,
        )
        dictionary = method(
            **args, output_type="molsysmt.InteractionsDict", heavy_mode="force"
        )
        assert msm.get_form(dictionary) == "molsysmt.InteractionsDict"
        restored = msm.convert(dictionary, to_form="molsysmt.Interactions")
        same(
            restored,
            msm.interactions.hbonds.get_hbonds(view.molsys, **args, heavy_mode="force"),
        )
        eager = method(
            selection=[0, 1, 2], structure_indices=[2, 0], pbc=False, heavy_mode="off"
        )
        for field in [
            "measurements",
            "measure_units",
            "participant_atoms",
            "evaluated_structure_indices",
        ]:
            same(getattr(restored, field), getattr(eager, field))
        assert restored.execution_records and eager.execution_records


@pytest.mark.parametrize("name", LEGACY)
def test_legacy_supplied_acceptors_and_native_unsupported_secondary_contracts(name):
    with msv.new_view(hbond_system()) as view:
        method = getattr(target(view, name), name)
        roles = dict(
            donors=np.array([[0, 2]], dtype=np.int64),
            acceptors=np.array([1], dtype=np.int64),
        )
        # The native supplied-donor route is independently reported; supported
        # precomputed acceptors still work with automatically recognized donors.
        result = method(acceptors=roles["acceptors"], pbc=False)
        same(result, native(name)(view.molsys, acceptors=roles["acceptors"], pbc=False))
        for kwargs in [
            dict(molecular_system_2=view.molsys),
            dict(**roles, output_type="molsysmt.Interactions"),
            dict(structure_indices_2=[0], output_type="molsysmt.Interactions"),
        ]:
            with pytest.raises(Exception) as error:
                native(name)(view.molsys, **kwargs)
            with pytest.raises(type(error.value)):
                method(**kwargs)
        np.testing.assert_array_equal(roles["donors"], [[0, 2]])
        np.testing.assert_array_equal(roles["acceptors"], [1])


@pytest.mark.parametrize("view", NAMES, indirect=True)
@pytest.mark.parametrize(
    "box", [np.eye(3), np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])]
)
def test_stored_periodic_images_reconstruct_physical_measurements(view, request, box):
    name = request.node.callspec.params["view"]
    source = (
        sulfur_system(periodic=True)
        if name == "get_disulfide_candidates"
        else hbond_system(periodic=True)
    )
    source.structures.box = puw.quantity(np.repeat(box[None], 3, axis=0), "nm")
    view.load(source, mode="replace")
    analysis = getattr(target(view, name), name)(
        structure_indices=[0], pbc=True, output_type="molsysmt.Interactions"
    )
    assert analysis.n_interactions == 1
    assert analysis.image_vectors is not None
    xyz = (
        puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[
            0, analysis.participant_atoms
        ]
        + analysis.image_vectors @ box
    )
    if name == "get_disulfide_candidates":
        distance = np.linalg.norm(xyz[1] - xyz[0])
    else:
        distance = np.linalg.norm(
            xyz[2] - xyz[0 if name == "get_luzard_chandler_hbonds" else 1]
        )
    key = "hydrogen_acceptor_distance" if name == "get_hbonds" else "distance"
    np.testing.assert_allclose(analysis.measurements[key], [distance], atol=1e-12)
    np.testing.assert_allclose(
        distance,
        0.20
        if name == "get_disulfide_candidates"
        else (0.28 if name == "get_luzard_chandler_hbonds" else 0.18),
        atol=1e-12,
    )


@pytest.mark.parametrize("view", NAMES, indirect=True)
def test_named_h5msm_roundtrip_uses_an_explicit_independent_system(
    view, request, tmp_path
):
    name = request.node.callspec.params["view"]
    analysis = getattr(target(view, name), name)(
        structure_indices=[2, 1, 0], pbc=False, output_type="molsysmt.Interactions"
    )
    independent = view.addons.molsysmt.basic.copy()
    independent.interactions = {**independent.interactions, "calculated": analysis}
    path = str(tmp_path / "detected.h5msm")
    msm.convert(independent, to_form=path)
    restored = msm.convert(path).interactions["calculated"]
    same(restored, analysis)
    np.testing.assert_array_equal(
        restored.query().to_dict()["occurrence_indices"],
        analysis.query().to_dict()["occurrence_indices"],
    )
    assert set(view.molsys.interactions) == {"preserve"}


def test_disulfides_keep_native_group_filters_and_already_recorded_bonds():
    with msv.new_view(sulfur_system(with_bond=True)) as view:
        method = view.addons.molsysmt.interactions.disulfides.get_disulfide_candidates
        assert msm.get(view.molsys, n_bonds=True) == 1
        assert len(method(structure_indices=[0], selection=[0], pbc=False)[0][0]) == 0
        assert len(method(structure_indices=[0], pbc=False)[0][0]) == 1
        extended = method(
            structure_indices=[0],
            group_names=["CYS", "MET"],
            max_bond_length=".3 nm",
            sorted=False,
            pbc=False,
        )
        assert len(extended[0][0]) == 3
        assert msm.get(view.molsys, n_bonds=True) == 1


@pytest.mark.parametrize("view", NAMES, indirect=True)
def test_native_invalid_arguments_propagate_without_source_or_scene_update(
    view, request
):
    name = request.node.callspec.params["view"]
    before = view.export_state()
    kwargs = dict(output_type="not-a-native-output")
    with pytest.raises(Exception) as error:
        native(name)(view.molsys, **kwargs)
    with pytest.raises(type(error.value)):
        getattr(target(view, name), name)(**kwargs)
    assert view.export_state() == before


@pytest.mark.parametrize("view", NAMES, indirect=True)
def test_pending_reads_replacement_closed_empty_and_cached_family_handles(
    view, request
):
    name = request.node.callspec.params["view"]
    method = getattr(target(view, name), name)
    view.addons.molsysmt.structure.translate(
        translation="[1, 0, 0] nm", in_place=True, update_view=False
    )
    pending = view.addons.molsysmt.get_sync_status()
    method(pbc=False)
    assert (
        view.addons.molsysmt.get_sync_status() == pending
        and pending["state"] == "pending"
    )
    with pytest.raises(SystemEditPendingError):
        view.export_state()
    view.addons.molsysmt.sync_view()
    source = (
        sulfur_system(with_bond=True)
        if name == "get_disulfide_candidates"
        else hbond_system()
    )
    view.load(source, mode="replace")
    same(method(pbc=False), native(name)(view.molsys, pbc=False))
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method(pbc=False)
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(target(empty, name), name)()


@pytest.mark.parametrize("name", LEGACY)
def test_classic_detector_receives_real_pentalanine_with_selected_local_axes(name):
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as view:
            args = dict(
                structure_indices=[2, 0], pbc=False, output_type="molsysmt.Interactions"
            )
            result = getattr(target(view, name), name)(**args)
            same(result, native(name)(view.molsys, **args))
            assert result.n_atoms == view.molsys.get_n_atoms()
            assert result.n_structures == 3
            assert set(result.evaluated_structure_indices) == {0, 2}
            assert not view.molsys.interactions
