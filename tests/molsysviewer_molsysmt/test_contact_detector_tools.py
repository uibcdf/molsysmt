"""Receive three explicit chemical detector contracts through the bound primary."""

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
FAMILIES = ("ionic", "hydrophobic", "halogen_bonds")
NAMES = {
    "ionic": "get_ionic_interactions",
    "hydrophobic": "get_hydrophobic_interactions",
    "halogen_bonds": "get_halogen_bonds",
}
SCOPES = {
    "ionic": ([0], [1]),
    "hydrophobic": ([1], [4]),
    "halogen_bonds": ([0, 1], [2, 3]),
}
ROLES = {
    "ionic": ("positive", "negative"),
    "hydrophobic": ("hydrophobic_1", "hydrophobic_2"),
    "halogen_bonds": ("donor", "halogen", "acceptor", "acceptor_reference"),
}
ATOMS = {"ionic": [0, 1], "hydrophobic": [1, 4], "halogen_bonds": [0, 1, 3, 2]}


def system(family):
    if family == "ionic":
        smiles = "[Na+].[Cl-]"
        xyz = [[0, 0, 0], [0.3, 0, 0]]
        moving = [1]
    elif family == "hydrophobic":
        smiles = "CCC.CCC"
        xyz = [
            [0, 0, 0],
            [0.15, 0, 0],
            [0.30, 0, 0],
            [0, 0.3, 0],
            [0.15, 0.3, 0],
            [0.30, 0.3, 0],
        ]
        moving = [3, 4, 5]
    else:
        smiles = "CCl.C=O"
        xyz = [[-0.15, 0, 0], [0, 0, 0], [0.36, 0.12 * np.sqrt(0.75), 0], [0.30, 0, 0]]
        moving = [2, 3]
    molsys = msm.convert(Chem.MolFromSmiles(smiles))
    coordinates = np.repeat(np.asarray(xyz)[None], 3, axis=0)
    coordinates[1, moving] += [0, 1, 0]
    molsys.structures.append(
        coordinates=puw.quantity(coordinates, "nm"),
        structure_id=["external-90", "external-12", "external-500"],
    )
    return molsys


def options(family):
    return dict(distance_threshold="0.4 nm") if family == "ionic" else {}


def native(family):
    return getattr(getattr(msm.interactions, family), NAMES[family])


def bound(view, family):
    return getattr(getattr(view.addons.molsysmt.interactions, family), NAMES[family])


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
        for a, b in zip(actual, expected):
            same(a, b)
    else:
        np.testing.assert_equal(actual, expected)


@pytest.fixture(params=FAMILIES)
def view(request):
    with msv.new_view(system(request.param)) as result:
        result.regions.add(selection=[0], tag="preserve")
        result.interactions.attach(
            msm.Interactions.from_records(
                [],
                n_atoms=result.molsys.get_n_atoms(),
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.contacts",
            ),
            name="sentinel",
            assume_aligned=True,
        )
        yield request.param, result


def test_explicit_signature_help_defaults_and_independent_navigation(view):
    family, value = view
    method = bound(value, family)
    signature = inspect.signature(native(family))
    assert inspect.signature(method) == signature.replace(
        parameters=list(signature.parameters.values())[1:]
    )
    assert method.digestion_plan is not None
    assert dir(getattr(value.addons.molsysmt.interactions, family)) == [NAMES[family]]
    assert not hasattr(value.addons.molsysmt, NAMES[family])
    assert not hasattr(value.addons.molsysmt.interactions, "metal_coordination")
    doc = inspect.getdoc(method)
    assert "not a scene object" in doc and "experimental" in doc
    assert "RSS" in doc and "not global identities" in doc
    assert isinstance(method(**options(family), pbc=False), msm.Interactions)
    for args in [
        dict(update_view=False),
        dict(molecular_system=value.molsys),
        dict(prepare=True),
    ]:
        with pytest.raises(UnknownArgumentError):
            method(**options(family), **args)
    if family == "ionic":
        with pytest.raises(TypeError):
            method()


@pytest.mark.parametrize("skip", [False, True])
def test_native_parity_readonly_source_scene_named_analysis_and_quantities(view, skip):
    family, value = view
    source = value.molsys
    atoms = source.topology.atoms.copy(deep=True)
    chemistry = source.chemical_states._states[0].bonds.copy(deep=True)
    xyz = puw.get_value(source.structures.coordinates).copy()
    state = value.export_state()
    sentinel = source.interactions["sentinel"]
    saved = deepcopy(sentinel.to_dict())
    args = dict(
        options(family),
        structure_indices=[2, 1, 0, 2],
        pbc=False,
        skip_digestion=skip,
        output_type="molsysmt.interactions",
    )
    if family == "ionic":
        args["distance_threshold"] = puw.quantity(0.4, "nm")
    with puw.context(standard_units=["angstrom", "degrees", "ps", "e"]):
        result = bound(value, family)(**args)
        expected = native(family)(source, **args)
    same(result, expected)
    assert result.n_interactions == 2
    assert result.participant_atoms.tolist() == ATOMS[family]
    assert result.participant_roles == ROLES[family]
    assert result.evaluated_structure_indices.tolist() == [0, 1, 2]
    assert result.occurrence_structures.tolist() == [0, 2]
    np.testing.assert_allclose(result.measurements["distance"], 0.3)
    assert result.measure_units["distance"] == "nm"
    if family == "ionic":
        assert result.measure_units["positive_charge"] == "e"
        np.testing.assert_allclose(result.measurements["positive_charge"], 1)
        np.testing.assert_allclose(result.measurements["negative_charge"], -1)
    if family == "halogen_bonds":
        assert result.measure_units["donor_angle"] == "radians"
        assert result.measure_units["acceptor_angle"] == "radians"
        np.testing.assert_allclose(result.measurements["donor_angle"], np.pi)
        np.testing.assert_allclose(result.measurements["acceptor_angle"], 2 * np.pi / 3)
    assert value.molsys is source and value.export_state() == state
    pd.testing.assert_frame_equal(source.topology.atoms, atoms)
    pd.testing.assert_frame_equal(source.chemical_states._states[0].bonds, chemistry)
    np.testing.assert_array_equal(puw.get_value(source.structures.coordinates), xyz)
    assert (
        set(source.interactions) == {"sentinel"}
        and source.interactions["sentinel"] is sentinel
    )
    same(sentinel.to_dict(), saved)
    assert result.parameters["attribution"]["items"] and result.software["molsysmt"]
    value.close()
    assert result.query().n_interactions == 2


@pytest.mark.parametrize(
    "mode,scope,count",
    [
        ("internal", "both", 2),
        ("internal", "first", 0),
        ("incident", "first", 2),
        ("incident", "second", 2),
        ("between", "first", 2),
        ("between", "second", 2),
    ],
)
def test_native_membership_roles_and_sparse_nonconsecutive_scopes(
    view, mode, scope, count
):
    family, value = view
    first, second = SCOPES[family]
    if scope == "second":
        first, second = second, first
    args = dict(
        options(family),
        selection_mode=mode,
        selection=first + second if scope == "both" else first,
        structure_indices=[2, 0, 2],
        pbc=False,
    )
    if mode == "between":
        args["selection_2"] = second
    result = bound(value, family)(**args)
    same(result, native(family)(value.molsys, **args))
    assert result.n_interactions == count
    assert result.evaluated_structure_indices.tolist() == [0, 2]
    assert 1 not in result.evaluated_structure_indices
    if count:
        assert result.participant_atoms.tolist() == ATOMS[family]
        assert (
            result.query(atom_indices=first, mode="involving_selection").n_interactions
            == 2
        )
        assert (
            result.query(atom_indices=first, mode="within_selection").n_interactions
            == 0
        )
        assert (
            result.between_selections(first, second, exclusive=True).n_interactions == 2
        )


def test_empty_evaluated_unevaluated_and_occurrence_indices(view):
    family, value = view
    method = bound(value, family)
    result = method(**options(family), structure_indices=[2, 0, 2], pbc=False)
    ids = result.query().to_dict()["occurrence_indices"]
    assert ids.dtype == np.int64 and len(np.unique(ids)) == 2
    for frame in [0, 2]:
        filtered = result.query(structure_indices=[frame]).to_dict()[
            "occurrence_indices"
        ]
        assert len(filtered) == 1 and filtered[0] in ids
    empty = method(**options(family), structure_indices=[1], pbc=False)
    assert empty.n_interactions == 0 and empty.evaluated_structure_indices.tolist() == [
        1
    ]
    assert all(v.shape == (0,) for v in empty.measurements.values())
    unassessed = method(**options(family), structure_indices=[], pbc=False)
    assert unassessed.evaluated_structure_indices.tolist() == []


@pytest.mark.parametrize("heavy_mode", ["off", "force"])
def test_typed_results_execution_and_explicit_named_h5msm_on_independent_copy(
    view, heavy_mode, tmp_path
):
    family, value = view
    args = dict(
        options(family), structure_indices=[2, 0, 2], pbc=False, heavy_mode=heavy_mode
    )
    dictionary = bound(value, family)(**args, output_type="molsysmt.InteractionsDict")
    assert msm.get_form(dictionary) == "molsysmt.InteractionsDict"
    analysis = msm.convert(dictionary, to_form="molsysmt.Interactions")
    same(analysis, native(family)(value.molsys, **args))
    assert analysis.execution_records
    independent = value.addons.molsysmt.basic.copy()
    independent.interactions = {**independent.interactions, "calculated": analysis}
    path = str(tmp_path / "contacts.h5msm")
    msm.convert(independent, to_form=path)
    loaded = msm.convert(path).interactions["calculated"]
    same(loaded, analysis)
    assert set(value.molsys.interactions) == {"sentinel"}


def test_external_selection_syntax_and_threshold_changes_remain_scientific(view):
    family, value = view
    args = dict(
        options(family),
        selection="index " + " ".join(map(str, range(value.molsys.get_n_atoms()))),
        syntax="MDTraj",
        pbc=False,
    )
    result = bound(value, family)(**args)
    same(result, native(family)(value.molsys, **args))
    assert result.n_interactions == 2
    args["distance_threshold"] = "2 angstrom"
    assert bound(value, family)(**args).n_interactions == 0
    if family == "halogen_bonds":
        args["distance_threshold"] = ".35 nm"
        args["donor_angle_range"] = puw.quantity([100, 120], "degrees")
        assert bound(value, family)(**args).n_interactions == 0


@pytest.mark.parametrize(
    "box",
    [
        np.eye(3),
        np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]]),
        np.array([[1, 0.1, 0], [0, 1, 0.1], [0, 0, 1]]),
    ],
)
def test_periodic_images_reconstruct_distances_and_halogen_angles(view, box):
    family, value = view
    source = system(family)
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    shifts = np.zeros((source.get_n_atoms(), 3), dtype=np.int64)
    if family == "halogen_bonds":
        shifts[:] = [[1, 0, 0], [0, 0, 0], [-1, 1, 0], [0, 1, 0]]
    else:
        shifts[ATOMS[family][1]] = [1, -1, 0]
    xyz += shifts @ box
    source.structures.coordinates = puw.quantity(xyz, "nm")
    source.structures.box = puw.quantity(np.repeat(box[None], 3, axis=0), "nm")
    value.load(source, mode="replace")
    result = bound(value, family)(**options(family), structure_indices=[0])
    same(result, native(family)(value.molsys, **options(family), structure_indices=[0]))
    assert result.n_interactions == 1 and result.image_vectors is not None
    observed = xyz[0, result.participant_atoms] + result.image_vectors @ box
    if family == "halogen_bonds":
        dx, xa, ar = (
            observed[1] - observed[0],
            observed[2] - observed[1],
            observed[3] - observed[2],
        )
        np.testing.assert_allclose(
            np.arccos(np.dot(-dx, xa) / np.linalg.norm(dx) / np.linalg.norm(xa)),
            result.measurements["donor_angle"][0],
        )
        np.testing.assert_allclose(
            np.arccos(np.dot(-xa, ar) / np.linalg.norm(xa) / np.linalg.norm(ar)),
            result.measurements["acceptor_angle"][0],
        )
        distance = np.linalg.norm(xa)
    else:
        distance = np.linalg.norm(observed[1] - observed[0])
    np.testing.assert_allclose(distance, 0.3, atol=1e-12)
    np.testing.assert_allclose(result.measurements["distance"], [distance], atol=1e-12)


@pytest.mark.parametrize(
    "invalid",
    [
        dict(selection_mode="between"),
        dict(selection_mode="cross"),
        dict(method="energy"),
        dict(distance_threshold="1 ps"),
        dict(output_type="tuple"),
        dict(structure_indices=[3]),
        dict(selection_2=[1]),
    ],
)
def test_native_errors_propagate_with_source_and_scene_unchanged(view, invalid):
    family, value = view
    args = options(family)
    args.update(invalid)
    before = value.export_state()
    with pytest.raises(Exception) as error:
        native(family)(value.molsys, **args)
    with pytest.raises(type(error.value)):
        bound(value, family)(**args)
    assert value.export_state() == before and set(value.molsys.interactions) == {
        "sentinel"
    }


def test_cached_reader_lifetime_pending_and_replacement(view):
    family, value = view
    method = bound(value, family)
    value.addons.molsysmt.structure.translate(
        translation="[1, 0, 0] nm", in_place=True, update_view=False
    )
    status = value.addons.molsysmt.get_sync_status()
    same(
        method(**options(family), pbc=False),
        native(family)(value.molsys, **options(family), pbc=False),
    )
    assert (
        value.addons.molsysmt.get_sync_status() == status
        and status["state"] == "pending"
    )
    with pytest.raises(SystemEditPendingError):
        value.export_state()
    value.addons.molsysmt.sync_view()
    value.load(system(family), mode="replace")
    assert method(**options(family), pbc=False).n_interactions == 2
    value.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method(**options(family), pbc=False)
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            bound(empty, family)(**options(family))


def test_ionic_compound_membership_and_geometry_references_are_native():
    source = msm.convert(Chem.MolFromSmiles("CC(=O)[O-].[Na+]"))
    source.structures.append(
        coordinates=puw.quantity(
            [[[0.1, 0.1, 0], [0.12, 0, 0], [0.3, 0, 0], [0.3, 0.1, 0], [0, 0, 0]]], "nm"
        )
    )
    with msv.new_view(source) as value:
        method = bound(value, "ionic")
        result = method(".4 nm", selection=[1, 2, 3, 4], pbc=False)
        same(
            result,
            native("ionic")(value.molsys, ".4 nm", selection=[1, 2, 3, 4], pbc=False),
        )
        assert result.n_interactions == 1
        assert result.relation(0)["participants"][1]["atom_indices"].tolist() == [
            1,
            2,
            3,
        ]
        np.testing.assert_allclose(result.measurements["distance"], [0.3])
        assert (
            result.query(atom_indices=[1], mode="involving_selection").n_interactions
            == 1
        )
        with pytest.raises(msm.ArgumentError, match="cuts a compound"):
            method(".4 nm", selection=[2, 3, 4], selection_mode="incident", pbc=False)


@pytest.mark.parametrize("family", FAMILIES)
def test_real_pentalanine_rejects_missing_chemistry_without_implicit_preparation(
    family,
):
    with msv.demo["pentalanine"] as demo:
        with msv.new_view(demo.molsys, structure_indices=[0, 8, 3]) as value:
            args = dict(options(family), structure_indices=[2, 0], pbc=False)
            # The legacy H5MSM demo lacks declared formal charges/bond chemistry.
            # It is an honest rejection case, not a positive prepared fixture.
            reason = (
                "explicit formal charge"
                if family == "ionic"
                else "Bond chemistry columns are missing"
            )
            before = value.export_state()
            with pytest.raises(msm.StructuralInconsistencyError, match=reason):
                native(family)(value.molsys, **args)
            with pytest.raises(msm.StructuralInconsistencyError, match=reason):
                bound(value, family)(**args)
            assert msm.get(value.molsys, n_structures=True) == 3
            assert value.export_state() == before and not value.molsys.interactions
