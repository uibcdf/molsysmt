"""Receive detached graph/type/charge preparation without adopting its output."""

import inspect
from copy import deepcopy
from pathlib import Path

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError
from rdkit import Chem

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys

puw = msm.pyunitwizard
ARGS = {
    "infer_covalent_bonds": {"structure_indices": 1},
    "assign_autodock_atom_types": {"typing_scheme": "autodock4"},
    "assign_partial_charges": {"method": "gasteiger_marsili"},
}


def system(name):
    if name == "infer_covalent_bonds":
        builder = msm.MolSysBuilder()
        atoms = [
            builder.add_atom(atom_name=n, atom_type=t)
            for n, t in zip(
                ["N", "CA", "C", "O", "CB", "H", "HN1"],
                ["N", "C", "C", "O", "C", "H", "H"],
            )
        ]
        builder.add_group(atoms, group_name="ALA", group_id="100")
        builder.set_coordinates(puw.quantity(np.zeros((3, 7, 3)), "nm"))
        source = builder.build()
        source.chemical_states.add_bonds([[2, 3]])
        msm.set(
            source,
            element="bond",
            bond_type="covalent",
            bond_order=2,
            bond_evidence="explicit",
        )
    else:
        molecule = Chem.AddHs(Chem.MolFromSmiles("CO"))
        conformer = Chem.Conformer(molecule.GetNumAtoms())
        conformer.SetPositions(np.arange(18, dtype=float).reshape(-1, 3))
        molecule.AddConformer(conformer)
        source = msm.convert(molecule, to_form="molsysmt.MolSys")
        xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
        source.structures.append(
            coordinates=puw.quantity(np.concatenate([xyz + 1, xyz + 2]), "nm"),
            structure_id=[70, 200],
        )
    return source


def prepare_view(name):
    view = msv.new_view(system(name))
    view.regions.add(selection=[0], tag="keep")
    view.interactions.attach(
        msm.Interactions.from_records(
            [],
            n_atoms=view.molsys.get_n_atoms(),
            n_structures=3,
            evaluated_structure_indices=[0, 1, 2],
            method="receiving.detached-build",
        ),
        name="preserve",
        assume_aligned=True,
    )
    return view


def same(actual, expected):
    if isinstance(expected, MolSys):
        pd.testing.assert_frame_equal(
            actual.topology.atoms, expected.topology.atoms, check_frame_type=False
        )
        assert actual.chemical_states._inventory_equals(expected.chemical_states)
        np.testing.assert_array_equal(
            puw.get_value(actual.structures.coordinates, to_unit="nm"),
            puw.get_value(expected.structures.coordinates, to_unit="nm"),
        )
        for field in (
            "partial_charge",
            "atom_ff_type",
            "partial_charge_assignment",
            "atom_type_assignment",
            "forcefield",
        ):
            same(
                getattr(actual.molecular_mechanics, field),
                getattr(expected.molecular_mechanics, field),
            )
        assert set(actual.interactions) == set(expected.interactions)
        for key in expected.interactions:
            same(
                actual.interactions[key].to_dict(), expected.interactions[key].to_dict()
            )
    elif isinstance(expected, pd.DataFrame):
        pd.testing.assert_frame_equal(actual, expected)
    elif isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for key in expected:
            same(actual[key], expected[key])
    elif isinstance(expected, (list, tuple)):
        assert type(actual) is type(expected) and len(actual) == len(expected)
        for left, right in zip(actual, expected):
            same(left, right)
    elif puw.is_quantity(expected):
        assert puw.get_unit(actual) == puw.get_unit(expected)
        np.testing.assert_array_equal(puw.get_value(actual), puw.get_value(expected))
    else:
        np.testing.assert_equal(actual, expected)


def snapshot(view):
    return (
        view.molsys,
        None if view.molsys is None else view.molsys.copy(),
        deepcopy(view.export_state())
        if view.addons.molsysmt.get_sync_status()["state"] != "pending"
        else None,
        view.addons.molsysmt.get_sync_status(),
        (list(view.history._undo), list(view.history._redo)),
        deepcopy(view.widget.initial_messages),
    )


def unchanged(view, before):
    target, scientific, scene, status, history, messages = before
    assert view.molsys is target
    same(view.molsys, scientific)
    if scene is not None:
        assert view.export_state() == scene
    assert view.addons.molsysmt.get_sync_status() == status
    assert (view.history._undo, view.history._redo) == history
    assert view.widget.initial_messages == messages


@pytest.fixture(params=ARGS)
def case(request):
    name = request.param
    with prepare_view(name) as view:
        yield name, view


def test_fixed_expert_signatures_required_models_help_and_digestion(case):
    name, view = case
    method = getattr(view.addons.molsysmt.build, name)
    native = inspect.signature(getattr(msm.build, name))
    assert inspect.signature(method) == native.replace(
        parameters=list(native.parameters.values())[1:]
    )
    assert method.digestion_plan is not None
    assert name in dir(view.addons.molsysmt.build)
    assert not hasattr(view.addons.molsysmt, name)
    assert "separate molecular system" in inspect.getdoc(method)
    assert "no update_view control" in inspect.getdoc(method)
    assert "independent native diagnostic" not in inspect.getdoc(method)
    assert "\nmolecular_system :" not in inspect.getdoc(method)
    if name != "infer_covalent_bonds":
        required = "typing_scheme" if name == "assign_autodock_atom_types" else "method"
        assert (
            inspect.signature(method).parameters[required].default
            is inspect.Parameter.empty
        )
    for extra in [
        {"molecular_system": view.molsys},
        {"update_view": True},
        {"in_place": True},
    ]:
        with pytest.raises(UnknownArgumentError):
            method(**ARGS[name], **extra)
    with pytest.raises(ArgumentError):
        method(**ARGS[name], skip_digestion="yes")


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("report", [False, True])
def test_native_output_is_detached_and_keeps_the_scene_and_primary(case, skip, report):
    name, view = case
    before = snapshot(view)
    kwargs = dict(ARGS[name], skip_digestion=skip, return_report=report)
    actual = getattr(view.addons.molsysmt.build, name)(**kwargs)
    expected = getattr(msm.build, name)(view.molsys, **kwargs)
    same(actual, expected)
    output = actual["molecular_system"] if report else actual
    assert output is not view.molsys
    assert output.structures.n_structures == 3
    if name == "infer_covalent_bonds":
        pairs = output.chemical_states.get_bonds()[
            ["atom1_index", "atom2_index"]
        ].values.tolist()
        assert pairs == [[0, 1], [0, 5], [1, 2], [1, 4], [2, 3]]
        assert (
            len(
                output.interactions["preserve"].to_dict()["evaluated_structure_indices"]
            )
            == 0
        )
        if report:
            assert actual["report"]["n_added_bonds"] == 4
    elif name == "assign_autodock_atom_types":
        assert output.molecular_mechanics.atom_ff_type.tolist() == [
            "C",
            "OA",
            "H",
            "H",
            "H",
            "HD",
        ]
        assert (
            output.molecular_mechanics.atom_type_assignment["typing_scheme"]
            == "autodock4"
        )
    else:
        np.testing.assert_allclose(
            np.asarray(output.molecular_mechanics.partial_charge, dtype=float),
            [
                0.03194068372,
                -0.39963024356,
                0.05268663182,
                0.05268663182,
                0.05268663182,
                0.20962966439,
            ],
            rtol=0,
            atol=1e-10,
        )
        assert (
            output.molecular_mechanics.partial_charge_assignment["method"]
            == "gasteiger_marsili"
        )
    unchanged(view, before)
    if report:
        # Caller edits to evidence cannot overwrite output-bound attribution.
        saved = deepcopy(
            output.molecular_mechanics.partial_charge_assignment
            if name == "assign_partial_charges"
            else output.molecular_mechanics.atom_type_assignment
            if name == "assign_autodock_atom_types"
            else output.chemical_states.get_preparation_history()
        )
        actual["report"].clear()
        bound = (
            output.molecular_mechanics.partial_charge_assignment
            if name == "assign_partial_charges"
            else output.molecular_mechanics.atom_type_assignment
            if name == "assign_autodock_atom_types"
            else output.chemical_states.get_preparation_history()
        )
        same(bound, saved)
    output.topology.atoms.loc[0, "atom_name"] = "changed-output"
    unchanged(view, before)


@pytest.mark.parametrize("skip", [False, True])
def test_pending_edits_are_read_without_implicit_sync_or_adoption(case, skip):
    name, view = case
    tools = view.addons.molsysmt
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm").copy() + 3
    tools.basic.set(coordinates=puw.quantity(xyz, "nm"), update_view=False)
    assert tools.get_sync_status()["state"] == "pending"
    before = snapshot(view)
    output = getattr(tools.build, name)(**ARGS[name], skip_digestion=skip)
    np.testing.assert_array_equal(
        puw.get_value(output.structures.coordinates, to_unit="nm"), xyz
    )
    unchanged(view, before)


@pytest.mark.parametrize(
    "parameters",
    [{"method": "unknown"}, {"chemical_state": 99}, {"structure_indices": [99]}],
)
def test_invalid_native_requests_preserve_primary_and_scene(case, parameters):
    name, view = case
    before = snapshot(view)
    kwargs = dict(ARGS[name], **parameters)
    with pytest.raises(Exception) as expected:
        getattr(msm.build, name)(view.molsys, **kwargs)
    with pytest.raises(type(expected.value)) as actual:
        getattr(view.addons.molsysmt.build, name)(**kwargs)
    assert str(actual.value) == str(expected.value)
    unchanged(view, before)


def test_cached_handles_follow_replacement_and_reject_closed_or_empty_owners(case):
    name, view = case
    method = getattr(view.addons.molsysmt.build, name)
    replacement = system(name)
    coordinates = (
        puw.get_value(replacement.structures.coordinates, to_unit="nm").copy() + 7
    )
    msm.set(replacement, coordinates=puw.quantity(coordinates, "nm"))
    view.load(replacement, mode="replace")
    same(method(**ARGS[name]), getattr(msm.build, name)(view.molsys, **ARGS[name]))
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method(**ARGS[name], skip_digestion=True)
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt.build, name)(**ARGS[name])


@pytest.mark.parametrize(
    "name", ["assign_autodock_atom_types", "assign_partial_charges"]
)
@pytest.mark.parametrize("structures", ["all", [2, 0, 2], [1]])
def test_assignment_structures_resolve_chemistry_without_slicing_output(
    name, structures
):
    with prepare_view(name) as view:
        before = snapshot(view)
        actual = getattr(view.addons.molsysmt.build, name)(
            **ARGS[name], structure_indices=structures, return_report=True
        )
        same(
            actual,
            getattr(msm.build, name)(
                view.molsys,
                **ARGS[name],
                structure_indices=structures,
                return_report=True,
            ),
        )
        assert actual["molecular_system"].structures.n_structures == 3
        unchanged(view, before)


@pytest.mark.parametrize(
    "name", ["assign_autodock_atom_types", "assign_partial_charges"]
)
def test_multiple_state_assignment_rejects_without_modifying_the_source(name):
    source = system(name)
    source.chemical_states.append_state()
    with msv.new_view(source) as view:
        before = snapshot(view)
        with pytest.raises(StructuralInconsistencyError, match="chemical state"):
            getattr(view.addons.molsysmt.build, name)(**ARGS[name])
        unchanged(view, before)


@pytest.mark.parametrize("units", [["pm", "fs"], ["pm", "fs", "coulomb"]])
def test_stored_charges_and_total_declarations_keep_native_units(units):
    with prepare_view("assign_partial_charges") as view:
        before = snapshot(view)
        with puw.context(standard_units=units):
            policy = puw.configure.report()
            result = view.addons.molsysmt.build.assign_partial_charges(
                method="gasteiger_marsili",
                expected_total_charge=puw.quantity(0, "coulomb"),
                return_report=True,
            )
            assert puw.configure.report() == policy
        assert result["report"]["charge_unit"] == "elementary_charge"
        assert np.sum(
            result["molecular_system"].molecular_mechanics.partial_charge
        ) == pytest.approx(0, abs=1e-10)
        unchanged(view, before)


def test_explicit_forcefield_uses_real_openmm_without_assigning_the_view():
    source = msm.convert(str(Path(msm.__file__).parent / "data/pdb/ala3.pdb"))
    with msv.new_view(source) as view:
        before = snapshot(view)
        result = view.addons.molsysmt.build.assign_partial_charges(
            method="forcefield",
            forcefield="AMBER14",
            expected_total_charge=0,
            return_report=True,
        )
        output = result["molecular_system"]
        values = np.asarray(output.molecular_mechanics.partial_charge)
        assert values.sum() == pytest.approx(0, abs=1e-8)
        groups = output.topology.atoms["group_index"].to_numpy()
        names = output.topology.atoms["atom_name"].to_numpy()
        charges = {
            name: values[i]
            for i, (name, group) in enumerate(zip(names, groups))
            if group == 1
        }
        assert charges["N"] == pytest.approx(-0.4157)
        assert charges["H"] == pytest.approx(0.2719)
        assert charges["O"] == pytest.approx(-0.5679)
        assert result["report"]["software"]["openmm"]
        unchanged(view, before)
