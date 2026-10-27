"""Receive explicit chemical calculations without assigning results to the view."""

import inspect
from copy import deepcopy

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError
from molsysviewer.system_edits import SystemEditPendingError
from rdkit import Chem
from rdkit.Chem import AllChem, rdDepictor

import molsysmt as msm

puw = msm.pyunitwizard
ARGS = {
    "get_autodock_atom_types": {"typing_scheme": "autodock4"},
    "get_cip_stereochemistry": {},
    "get_partial_charges": {"method": "gasteiger_marsili"},
}


def system(smiles="CO", *, geometry=False):
    # Explicit fixture preparation precedes the view; readers cannot add H.
    molecule = Chem.AddHs(Chem.MolFromSmiles(smiles))
    if geometry:
        assert AllChem.EmbedMolecule(molecule, randomSeed=42) == 0
    else:
        rdDepictor.Compute2DCoords(molecule)
    source = msm.convert(molecule)
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    mirrored = xyz.copy()
    mirrored[:, :, 0] *= -1
    source.structures.append(
        coordinates=puw.quantity(np.concatenate([mirrored, xyz + [1, 0, 0]]), "nm"),
        structure_id=[70, 200],
    )
    return source


def call(view, name, *, native=False, **kwargs):
    args = dict(ARGS[name], **kwargs)
    if native:
        return getattr(msm.physchem, name)(view.molsys, **args)
    return getattr(view.addons.molsysmt.physchem, name)(**args)


def same(actual, expected):
    if isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for key in expected:
            same(actual[key], expected[key])
    elif puw.is_quantity(expected):
        assert puw.get_unit(actual) == puw.get_unit(expected)
        np.testing.assert_array_equal(puw.get_value(actual), puw.get_value(expected))
    elif isinstance(expected, (tuple, list)):
        assert type(actual) is type(expected) and len(actual) == len(expected)
        for a, e in zip(actual, expected):
            same(a, e)
    else:
        np.testing.assert_equal(actual, expected)


@pytest.fixture
def view():
    with msv.new_view(system()) as result:
        result.regions.add(selection=[1], tag="oxygen")
        result.interactions.attach(
            msm.Interactions.from_records(
                [],
                n_atoms=6,
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.assignments",
            ),
            name="preserve",
            assume_aligned=True,
        )
        yield result


@pytest.mark.parametrize("name", ARGS)
def test_exact_expert_signature_help_digestion_and_no_assignment_controls(view, name):
    method = getattr(view.addons.molsysmt.physchem, name)
    native = inspect.signature(getattr(msm.physchem, name))
    assert inspect.signature(method) == native.replace(
        parameters=list(native.parameters.values())[1:]
    )
    assert method.digestion_plan is not None
    assert not hasattr(view.addons.molsysmt, name)
    doc = inspect.getdoc(method)
    assert "current view.molsys" in doc and "not a scene object" in doc
    assert "\nmolecular_system :" not in doc
    for extra in [
        dict(molecular_system=view.molsys),
        dict(update_view=False),
        dict(prepare=True),
    ]:
        with pytest.raises(UnknownArgumentError):
            method(**ARGS[name], **extra)
        with pytest.raises(TypeError):
            method(**ARGS[name], **extra, skip_digestion=True)
    if name != "get_cip_stereochemistry":
        parameter = "method" if name == "get_partial_charges" else "typing_scheme"
        assert (
            inspect.signature(method).parameters[parameter].default
            is inspect.Parameter.empty
        )
    else:
        assert (
            inspect.signature(method).parameters["from_coordinates"].kind
            is inspect.Parameter.KEYWORD_ONLY
        )


@pytest.mark.parametrize("name", ARGS)
@pytest.mark.parametrize("selection", ["all", [5, 1, 5], "atom_type=='O'", []])
@pytest.mark.parametrize("skip", [False, True])
def test_full_graph_sorted_unique_empty_outputs_and_explicit_structures(
    view, name, selection, skip
):
    args = dict(selection=selection, structure_indices=[2, 0, 2], skip_digestion=skip)
    if name != "get_cip_stereochemistry":
        args["return_report"] = True
    actual = call(view, name, **args)
    same(actual, call(view, name, native=True, **args))
    indices = np.unique(msm.select(view.molsys, selection=selection)).astype(np.int64)
    np.testing.assert_array_equal(actual.get("report", actual)["atom_indices"], indices)
    if name == "get_autodock_atom_types":
        assert actual["atom_ff_type"].dtype == np.dtype("U2")
        assert actual["report"]["evaluated_atom_indices"].tolist() == list(range(6))
        np.testing.assert_array_equal(
            actual["atom_ff_type"], np.array(["C", "OA", "H", "H", "H", "HD"])[indices]
        )
    elif name == "get_partial_charges":
        assert actual["partial_charge"].shape == (len(indices),)
        assert actual["report"]["evaluated_atom_indices"].tolist() == list(range(6))
    else:
        pairs = actual["bonded_atom_pairs"]
        assert pairs.shape == (len(actual["bond_indices"]), 2)
        assert actual["bond_stereo_atom_indices"].shape == pairs.shape
        assert np.isin(pairs, indices).all()
        assert actual["atom_stereochemistry"].tolist() == [None] * len(indices)


@pytest.mark.parametrize("name", ARGS)
@pytest.mark.parametrize("state", [None, "reference"])
def test_group_free_external_selection_is_a_positive_numeric_equivalent(
    view, name, state
):
    actual = call(
        view, name, selection="index 1", syntax="MDTraj", chemical_state=state
    )
    same(actual, call(view, name, selection=[1], chemical_state=state, native=True))
    assert view.molsys.topology.n_groups == 0 and view.molsys.topology.n_chains == 0


@pytest.mark.parametrize("name", ARGS)
def test_nonreference_state_and_frame_associations_do_not_choose_a_visible_frame(name):
    source = system()
    state = source.chemical_states._states[0].copy()
    state.state_id = "independent-copy"
    source.chemical_states._append_state(state)
    msm.set(source, structure_chemical_state_index=[0, 1, 0])
    with msv.new_view(source) as result:
        same(
            call(result, name, chemical_state=1),
            call(result, name, chemical_state=1, native=True),
        )
        same(
            call(result, name, chemical_state="structure", structure_indices=[2, 0]),
            call(result, name),
        )
        with pytest.raises(msm.StructuralInconsistencyError):
            call(result, name, chemical_state="structure", structure_indices=[0, 1])
        assert result.molsys.chemical_states.reference_chemical_state_index == 0


@pytest.mark.parametrize("name", ARGS)
def test_output_arrays_scalar_metadata_and_primary_scene_coverage_are_preserved(
    view, name
):
    primary = view.molsys
    owners = (
        primary.topology,
        primary.structures,
        primary.chemical_states,
        primary.interactions["preserve"],
    )
    attrs = primary.chemical_states._states[0].atom_attributes.copy(deep=True)
    bonds = primary.chemical_states._states[0].bonds.copy(deep=True)
    xyz = puw.get_value(primary.structures.coordinates).copy()
    coverage = deepcopy(owners[-1].to_dict())
    scene, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    args = {} if name == "get_cip_stereochemistry" else dict(return_report=True)
    received = call(view, name, **args)
    if name == "get_cip_stereochemistry":
        received["atom_stereochemistry"][:] = "edited"
        received["atom_indices"][:] = -1
        received["software"]["rdkit"] = "edited"
        received["references"][0]["doi"] = "edited"
    else:
        key = "atom_ff_type" if name == "get_autodock_atom_types" else "partial_charge"
        if key == "atom_ff_type":
            received[key][:] = "XX"
        else:
            received[key][:] *= 2
        received["report"]["atom_indices"][:] = -1
        received["report"]["parameters"]["consumer_edit"] = True
        received["report"]["software"]["rdkit"] = "edited"
    same(call(view, name, **args), call(view, name, native=True, **args))
    assert view.molsys is primary
    assert all(
        a is b
        for a, b in zip(
            owners,
            (
                primary.topology,
                primary.structures,
                primary.chemical_states,
                primary.interactions["preserve"],
            ),
        )
    )
    pd.testing.assert_frame_equal(
        attrs, primary.chemical_states._states[0].atom_attributes
    )
    pd.testing.assert_frame_equal(bonds, primary.chemical_states._states[0].bonds)
    np.testing.assert_array_equal(xyz, puw.get_value(primary.structures.coordinates))
    same(coverage, owners[-1].to_dict())
    assert (
        view.export_state() == scene
        and view.addons.molsysmt.get_sync_status() == status
    )


@pytest.mark.parametrize("name", ARGS)
def test_pending_read_cached_replacement_and_closed_empty_view(view, name):
    method = getattr(view.addons.molsysmt.physchem, name)
    view.addons.molsysmt.structure.translate(
        translation=puw.quantity([1, 0, 0], "nm"), in_place=True, update_view=False
    )
    status = view.addons.molsysmt.get_sync_status()
    call(view, name)
    assert (
        status["state"] == "pending"
        and view.addons.molsysmt.get_sync_status() == status
    )
    with pytest.raises(SystemEditPendingError):
        view.export_state()
    view.addons.molsysmt.sync_view()
    view.load(system("[NH4+]"), mode="replace")
    same(method(**ARGS[name]), call(view, name, native=True))
    if name == "get_partial_charges":
        assert np.sum(
            puw.get_value(method(**ARGS[name]), to_unit="elementary_charge")
        ) == pytest.approx(1)
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method(**ARGS[name])
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            call(empty, name)


@pytest.mark.parametrize("name", ARGS)
@pytest.mark.parametrize(
    "kwargs",
    [dict(selection=[999]), dict(structure_indices=[999]), dict(chemical_state=99)],
)
def test_native_validation_errors_are_preserved_without_scene_changes(
    view, name, kwargs
):
    scene = view.export_state()
    with pytest.raises(Exception) as expected:
        call(view, name, native=True, **kwargs)
    with pytest.raises(type(expected.value)):
        call(view, name, **kwargs)
    assert view.export_state() == scene


def test_named_models_charge_units_total_checks_and_no_reuse(view):
    view.molsys.molecular_mechanics.partial_charge = np.full(6, 9.0)
    with puw.context(standard_units=["coulomb", "angstrom", "fs"]):
        result = call(
            view,
            "get_partial_charges",
            expected_total_charge=puw.quantity(0, "coulomb"),
            return_report=True,
        )
        assert puw.get_unit(result["partial_charge"]) == puw.unit("coulomb")
    values = puw.get_value(result["partial_charge"], to_unit="elementary_charge")
    np.testing.assert_allclose(values[:2], [0.0319, -0.3996], atol=5e-5, rtol=0)
    assert values.sum() == pytest.approx(0, abs=1e-10)
    np.testing.assert_array_equal(
        view.molsys.molecular_mechanics.partial_charge, [9.0] * 6
    )
    assert result["report"]["parameters"]["iterations"] == 12
    with pytest.raises(msm.StructuralInconsistencyError, match="conflicts"):
        call(view, "get_partial_charges", expected_total_charge=1)
    with puw.context(standard_units=["pm", "fs"]):
        with pytest.raises(Exception) as caught:
            call(view, "get_partial_charges")
        assert type(caught.value).__name__ == "NoStandardsError"


def test_declared_enantiomers_and_double_bond_labels_use_full_context():
    for smiles, expected in [("N[C@@H](C)C(=O)O", "S"), ("N[C@H](C)C(=O)O", "R")]:
        with msv.new_view(system(smiles)) as result:
            observed = call(result, "get_cip_stereochemistry", selection=[1])
            assert observed["atom_stereochemistry"].tolist() == [expected]
            assert observed["n_atoms"] > 1
            assert observed["bonded_atom_pairs"].shape == (0, 2)
            assert observed["evidence"] == "declared_stereochemistry"
    for smiles, expected in [("F/C=C/F", "E"), ("F/C=C\\F", "Z")]:
        with msv.new_view(system(smiles)) as result:
            observed = call(result, "get_cip_stereochemistry", selection=[2, 1, 2])
            assert observed["bond_stereochemistry"].tolist() == [expected]
            assert observed["bonded_atom_pairs"].tolist() == [[1, 2]]
            assert call(result, "get_cip_stereochemistry", selection=[1])[
                "bond_indices"
            ].shape == (0,)


def test_coordinate_inference_keeps_keyword_only_control_and_one_structure_requirement():
    with msv.new_view(system("N[C@@H](C)C(=O)O", geometry=True)) as result:
        for frame, expected in [(0, "S"), (1, "R"), (2, "S")]:
            actual = call(
                result,
                "get_cip_stereochemistry",
                from_coordinates=True,
                structure_indices=[frame],
                selection=[1],
            )
            assert actual["atom_stereochemistry"].tolist() == [expected]
            assert (
                actual["evidence"] == "coordinates"
                and actual["structure_index"] == frame
            )
            same(
                actual,
                call(
                    result,
                    "get_cip_stereochemistry",
                    native=True,
                    from_coordinates=True,
                    structure_indices=[frame],
                    selection=[1],
                ),
            )
        with pytest.raises(msm.StructuralInconsistencyError, match="exactly one"):
            call(result, "get_cip_stereochemistry", from_coordinates=True)
        assert call(result, "get_cip_stereochemistry", selection=[1])[
            "atom_stereochemistry"
        ].tolist() == ["S"]


def test_forcefield_charges_use_unchanged_real_alanine_template():
    with msv.new_view("molsysmt/data/pdb/ala3.pdb") as result:
        args = dict(
            method="forcefield",
            forcefield="AMBER14",
            expected_total_charge=0,
            return_report=True,
        )
        actual = call(result, "get_partial_charges", **args)
        same(actual, call(result, "get_partial_charges", native=True, **args))
        values = puw.get_value(actual["partial_charge"], to_unit="elementary_charge")
        names, groups = msm.get(
            result.molsys, element="atom", atom_name=True, group_index=True
        )
        center = {
            name: values[i]
            for i, (name, group) in enumerate(zip(names, groups))
            if group == 1
        }
        assert center["N"] == pytest.approx(-0.4157) and center["O"] == pytest.approx(
            -0.5679
        )
        assert values.sum() == pytest.approx(0, abs=1e-8)
        assert actual["report"]["software"]["openmm"]


@pytest.mark.parametrize("name", ARGS)
def test_unknown_inserted_chemistry_is_not_silently_prepared_after_499(name):
    source = msm.convert(Chem.MolFromSmiles("CO"))
    builder = msm.MolSysBuilder(source)
    builder.add_atom(atom_name="Ar", atom_type="Ar")
    extended = builder.build()
    extended.structures.append(coordinates=puw.quantity(np.zeros((1, 3, 3)), "nm"))
    with msv.new_view(extended) as result:
        before = result.export_state()
        with pytest.raises(msm.StructuralInconsistencyError):
            call(result, name)
        assert result.molsys.chemical_states.n_atoms == 3
        assert (
            result.molsys.chemical_states._states[0]
            .atom_attributes.iloc[-1]
            .isna()
            .all()
        )
        assert result.export_state() == before


@pytest.mark.parametrize(
    "name,kwargs",
    [
        ("get_autodock_atom_types", dict(typing_scheme="automatic")),
        ("get_autodock_atom_types", dict(method="automatic")),
        ("get_partial_charges", dict(method="automatic")),
        ("get_partial_charges", dict(method="forcefield")),
        ("get_partial_charges", dict(forcefield="AMBER14")),
        ("get_partial_charges", dict(expected_total_charge=puw.quantity(0, "nm"))),
        ("get_cip_stereochemistry", dict(engine="automatic")),
    ],
)
def test_unqualified_models_and_missing_explicit_parameters_are_not_substituted(
    view, name, kwargs
):
    with pytest.raises(Exception) as expected:
        call(view, name, native=True, **kwargs)
    with pytest.raises(type(expected.value)):
        call(view, name, **kwargs)


@pytest.mark.parametrize("name", ARGS)
def test_real_bundled_caffeine_readers_preserve_declared_h_inventory(name):
    molecule = Chem.SDMolSupplier(
        msm.systems["caffeine"]["caffeine.sdf"], removeHs=False
    )[0]
    assert molecule is not None and molecule.GetNumAtoms() == 24
    with msv.new_view(molecule) as result:
        before = result.export_state()
        same(call(result, name), call(result, name, native=True))
        assert result.molsys.get_n_atoms() == 24
        assert result.export_state() == before


def test_real_optional_attribution_keeps_native_scopes_without_consumer_credit(view):
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("bound assignment readers"):
        with ackredit.scope("consumer.chemical_readers"):
            for name in ARGS:
                call(view, name)
        children = ackredit.current_session().usage_tree["consumer.chemical_readers"][
            "children"
        ]
        assert set(children) == {"molsysmt.physchem." + name for name in ARGS} | {
            "molsysmt.physchem.get_aromaticity"
        }
        assert {
            "doi:10.1021/acs.jcim.8b00324",
            "doi:10.1016/0040-4020(80)80168-2",
        } <= set(ackredit.get_used_items())
