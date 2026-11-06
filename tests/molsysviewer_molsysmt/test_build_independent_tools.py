"""Receive native assembly and typed-H reduction without adopting their results."""

import inspect
import json
from copy import deepcopy

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt.native import Structures
from tests.build.test_merge_nonpolar_hydrogens import declared_methanol
from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
    same,
    snapshot,
    unchanged,
)
from tests.native.test_molsys import build_minimal_molsys

puw = msm.pyunitwizard
NAMES = ("make_bioassembly", "merge_nonpolar_hydrogens")


def operation(chains=(0, 1)):
    return {
        "chain_indices": list(chains),
        "rotations": [
            np.eye(3),
            np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]),
        ],
        "translations": puw.quantity([[0, 0, 0], [10, 20, 30]], "angstrom"),
    }


def assembly_source():
    source = build_minimal_molsys(3)
    source.structures = Structures(
        coordinates=source.structures.coordinates,
        time=puw.quantity([5, 15, 40], "ps"),
        structure_id=["label-A", "label-B", "label-C"],
        bioassembly={"one": operation()},
    )
    return source


def source_for(name):
    return assembly_source() if name == "make_bioassembly" else declared_methanol()


def parameters_for(name):
    return {} if name == "make_bioassembly" else {"typing_scheme": "autodock4"}


@pytest.fixture(params=NAMES)
def case(request):
    name = request.param
    with msv.new_view(source_for(name)) as view:
        view.regions.add(selection=[0], tag="keep")
        view.shapes.add_sphere(atom_indices=[0], tag="anchor")
        yield name, view


def test_signatures_documented_native_defaults_and_no_edit_controls(case):
    name, view = case
    method = getattr(view.addons.molsysmt.build, name)
    native = inspect.signature(getattr(msm.build, name))
    assert inspect.signature(method) == native.replace(
        parameters=list(native.parameters.values())[1:]
    )
    assert method.digestion_plan is not None
    assert name in dir(view.addons.molsysmt.build)
    assert not hasattr(view.addons.molsysmt, name)
    text = inspect.getdoc(method)
    assert "View integration" in text and "no update_view" in text
    for parameter in inspect.signature(method).parameters:
        assert f"{parameter} :" in text
    for key in ("molecular_system", "update_view", "in_place", "prepare"):
        with pytest.raises(UnknownArgumentError):
            method(**parameters_for(name), **{key: None})
    with pytest.raises(Exception):
        method(**parameters_for(name), skip_digestion="yes")


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("chains,atoms", [([0, 1], [0, 1, 2, 3]), ([[1], [1]], [2, 3])])
@pytest.mark.parametrize("indices", [[2, 0, 2], [1]])
def test_assembly_geometry_repeated_structure_order_units_and_source(
    unit, chains, atoms, indices
):
    with msv.new_view(assembly_source()) as view:
        before = snapshot(view)
        transform = operation(chains)
        transform_before = deepcopy(transform)
        source = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[
            indices
        ][:, atoms]
        rotated = np.stack(
            [-source[:, :, 1], source[:, :, 0], source[:, :, 2]], axis=-1
        )
        expected = np.concatenate([source, rotated + [1, 2, 3]], axis=1)
        with puw.context(standard_units=[unit, "ps", "radians"]):
            result = view.addons.molsysmt.build.make_bioassembly(
                bioassembly=transform, structure_indices=indices
            )
        assert result is not view.molsys
        assert result.get_n_atoms() == len(atoms) * 2
        np.testing.assert_allclose(
            puw.get_value(result.structures.coordinates, to_unit="nm"),
            expected,
            rtol=0,
            atol=1e-13,
        )
        assert result.structures.structure_id.tolist() == [
            ["label-A", "label-B", "label-C"][i] for i in indices
        ]
        np.testing.assert_array_equal(
            puw.get_value(result.structures.time, to_unit="ps"),
            np.array([5, 15, 40])[indices],
        )
        ids = msm.get(result, element="chain", chain_id=True)
        assert len(ids) == len(set(ids))
        same(transform, transform_before)
        unchanged(view, before)


@pytest.mark.parametrize("assembly", [None, "one"])
@pytest.mark.parametrize("skip", [False, True])
def test_stored_assembly_and_first_structure_default(assembly, skip):
    with msv.new_view(assembly_source()) as view:
        before = snapshot(view)
        result = view.addons.molsysmt.build.make_bioassembly(
            bioassembly=assembly, skip_digestion=skip
        )
        expected = msm.build.make_bioassembly(
            view.molsys, bioassembly=assembly, skip_digestion=skip
        )
        same(result, expected)
        assert result.structures.n_structures == 1
        assert result.structures.structure_id.tolist() == ["label-A"]
        unchanged(view, before)


def test_real_bundled_barnase_assembly_has_unique_ids_and_preserves_names():
    source = msm.convert(msm.systems["Barnase-Barstar"]["1brs.bcif.gz"])
    with msv.new_view(source) as view:
        before = snapshot(view)
        stored = msm.get(view.molsys, bioassembly=True)["1"]
        chains = np.arange(msm.get(view.molsys, n_chains=True))
        transform = {
            "chain_indices": [chains] * 3,
            "rotations": [stored["rotations"][0]] * 3,
            "translations": [stored["translations"][0]] * 3,
        }
        names = msm.get(view.molsys, element="chain", chain_name=True)
        result = view.addons.molsysmt.build.make_bioassembly(transform)
        ids = msm.get(result, element="chain", chain_id=True)
        assert ids == list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + [
            "AA",
            "AB",
            "AC",
            "AD",
            "AE",
            "AF",
            "AG",
            "AH",
            "AI",
            "AJ",
        ]
        assert msm.get(result, element="chain", chain_name=True) == names * 3
        assert result.get_n_atoms() == view.molsys.get_n_atoms() * 3
        unchanged(view, before)


@pytest.mark.parametrize("indices", [[2, 0], [2, 0, 2], "all"])
@pytest.mark.parametrize("report", [False, True])
@pytest.mark.parametrize("skip", [False, True])
def test_projection_has_analytic_charge_transfers_and_explicit_identity(
    indices, report, skip
):
    with msv.new_view(declared_methanol()) as view:
        analysis = msm.Interactions.from_records(
            [],
            n_atoms=6,
            n_structures=3,
            evaluated_structure_indices=[0, 2],
            method="receiving.typed-projection",
        )
        view.interactions.attach(analysis, name="science", assume_aligned=True)
        before = snapshot(view)
        result = view.addons.molsysmt.build.merge_nonpolar_hydrogens(
            "autodock4",
            structure_indices=indices,
            return_report=report,
            skip_digestion=skip,
        )
        output = result["molecular_system"] if report else result
        assert output is not view.molsys and output.get_n_atoms() == 3
        assert output.topology.atoms.atom_id.tolist() == ["17", "3", "11"]
        assert output.molecular_mechanics.atom_ff_type.tolist() == ["C", "OA", "HD"]
        np.testing.assert_allclose(
            np.asarray(output.molecular_mechanics.partial_charge, dtype=float),
            [0.2, -0.5, 0.3],
            rtol=0,
            atol=1e-12,
        )
        frames = [0, 1, 2] if isinstance(indices, str) else indices
        np.testing.assert_array_equal(
            puw.get_value(output.structures.coordinates, to_unit="nm"),
            puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[frames][
                :, [0, 1, 5]
            ],
        )
        assert not output.interactions
        assert msm.get(output, selection=[0], n_explicit_hydrogens=True) == [3]
        assert msm.get(output, selection=[0], allows_implicit_hydrogens=True) == [False]
        if report:
            values = result["report"]
            assert values["schema"] == "molsysmt.atom_projection@1"
            np.testing.assert_array_equal(
                values["output_to_source_atom_indices"], [0, 1, 5]
            )
            np.testing.assert_array_equal(
                values["source_to_output_atom_indices"], [0, 1, -1, -1, -1, 2]
            )
            np.testing.assert_array_equal(
                values["merged_source_atom_pairs"], [[2, 0], [3, 0], [4, 0]]
            )
            assert values["charge_unit"] == "elementary_charge"
            np.testing.assert_allclose(
                values["charge_transfers"], [0.1, 0.2, 0.3], rtol=0, atol=1e-12
            )
            assert (
                abs(values["selected_total_charge"] - values["output_total_charge"])
                <= values["charge_conservation_tolerance"]
            )
            assert values["source_structure_indices"].tolist() == frames
            assert values["invalidated_interaction_names"] == ["science"]
        unchanged(view, before)


@pytest.mark.parametrize("length_unit", ["angstrom", "pm"])
def test_projection_report_keeps_charge_unit_under_nondefault_policy(length_unit):
    with msv.new_view(declared_methanol()) as view:
        before = snapshot(view)
        with puw.context(standard_units=[length_unit, "ps", "radians", "coulomb"]):
            result = view.addons.molsysmt.build.merge_nonpolar_hydrogens(
                "autodock4", return_report=True
            )
        assert result["report"]["charge_unit"] == "elementary_charge"
        np.testing.assert_allclose(
            result["report"]["charge_transfers"], [0.1, 0.2, 0.3]
        )
        np.testing.assert_array_equal(
            puw.get_value(
                result["molecular_system"].structures.coordinates, to_unit="nm"
            ),
            puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[
                :, [0, 1, 5]
            ],
        )
        unchanged(view, before)


def test_projection_selection_and_typing_keep_omission_distinct_from_merging():
    source = declared_methanol()
    with msv.new_view(source) as view:
        before = snapshot(view)
        result = view.addons.molsysmt.build.merge_nonpolar_hydrogens(
            "autodock4", selection=[4, 0, 2, 4], return_report=True
        )
        report = result["report"]
        assert report["selected_source_atom_indices"].tolist() == [0, 2, 4]
        assert report["omitted_source_atom_indices"].tolist() == [1, 3, 5]
        assert report["merged_source_atom_pairs"].tolist() == [[2, 0], [4, 0]]
        assert report["output_to_source_atom_indices"].tolist() == [0]
        np.testing.assert_allclose(
            np.asarray(
                result["molecular_system"].molecular_mechanics.partial_charge,
                dtype=float,
            ),
            [0],
            rtol=0,
            atol=report["charge_conservation_tolerance"],
        )
        unchanged(view, before)
    source.molecular_mechanics.atom_ff_type = ["C", "OA", "HD", "H", "H", "HD"]
    with msv.new_view(source) as view:
        report = view.addons.molsysmt.build.merge_nonpolar_hydrogens(
            "autodock4", return_report=True
        )["report"]
        assert report["output_to_source_atom_indices"].tolist() == [0, 1, 2, 5]


@pytest.mark.parametrize("chemical_state", ["reference", 0, "structure"])
@pytest.mark.parametrize(
    "selection,syntax",
    [
        ("all", "MolSysMT"),
        (list(range(6)), "MolSysMT"),
        ([5, 4, 3, 2, 1, 0, 2], "MolSysMT"),
        ("all", "MDTraj"),
    ],
)
def test_projection_state_and_selection_syntax_are_native(
    chemical_state, selection, syntax
):
    with msv.new_view(declared_methanol()) as view:
        before = snapshot(view)
        result = view.addons.molsysmt.build.merge_nonpolar_hydrogens(
            "autodock4",
            chemical_state=chemical_state,
            selection=selection,
            syntax=syntax,
            return_report=True,
        )
        assert result["report"]["output_to_source_atom_indices"].tolist() == [0, 1, 5]
        assert result["report"]["chemical_state_index"] == 0
        np.testing.assert_allclose(
            np.asarray(
                result["molecular_system"].molecular_mechanics.partial_charge,
                dtype=float,
            ),
            [0.2, -0.5, 0.3],
            rtol=0,
            atol=1e-12,
        )
        unchanged(view, before)


def test_projection_report_composition_detached_metadata_and_public_output_edit():
    with msv.new_view(declared_methanol()) as view:
        before = snapshot(view)
        result = view.addons.molsysmt.build.merge_nonpolar_hydrogens(
            "autodock4", return_report=True
        )
        report = result["report"]
        composed = view.addons.molsysmt.basic.compose_atom_maps([report])
        assert composed["output_to_source_atom_indices"].tolist() == [0, 1, 5]
        assert composed["source_to_representative_atom_indices"].tolist() == [
            0,
            1,
            0,
            0,
            0,
            2,
        ]
        portable = json.loads(json.dumps(report, default=lambda value: value.tolist()))
        assert portable["charge_unit"] == "elementary_charge"
        assert (
            report["attribution"]["target"] == "molsysmt.build.merge_nonpolar_hydrogens"
        )
        report["output_to_source_atom_indices"][:] = -1
        report["references"][0]["roles"].append("caller-edit")
        later = view.addons.molsysmt.build.merge_nonpolar_hydrogens(
            "autodock4", return_report=True
        )
        assert later["report"]["output_to_source_atom_indices"].tolist() == [0, 1, 5]
        assert later["report"]["references"][0]["roles"] == ["reference_implementation"]
        output = result["molecular_system"]
        msm.set(
            output,
            coordinates=puw.quantity(
                puw.get_value(output.structures.coordinates, to_unit="nm") + 5, "nm"
            ),
        )
        unchanged(view, before)


def test_real_caffeine_typing_and_charge_provenance_are_retained():
    molecule = msm.convert(msm.systems["caffeine"]["caffeine.sdf"], to_form="rdkit.Mol")
    source = msm.build.assign_autodock_atom_types(molecule, typing_scheme="autodock4")
    source = msm.build.assign_partial_charges(source, method="gasteiger_marsili")
    with msv.new_view(source) as view:
        before = snapshot(view)
        result = view.addons.molsysmt.build.merge_nonpolar_hydrogens(
            "autodock4", return_report=True
        )
        output = result["molecular_system"]
        assert output.get_n_atoms() == 14
        assignment = output.molecular_mechanics.partial_charge_assignment
        assert assignment["status"] == "derived"
        assert assignment["method"] == "nonpolar_hydrogen_charge_aggregation"
        assert assignment["source_assignment"]["method"] == "gasteiger_marsili"
        assert (
            assignment["source_assignment"]["software"]
            == view.molsys.molecular_mechanics.partial_charge_assignment["software"]
        )
        assert output.molecular_mechanics.atom_type_assignment["status"] == "derived"
        assert result["report"]["selected_total_charge"] == pytest.approx(
            result["report"]["output_total_charge"], abs=1e-12
        )
        unchanged(view, before)


@pytest.mark.parametrize(
    "parameters",
    [
        {"structure_indices": [-1]},
        {"structure_indices": [3]},
        {"bioassembly": "missing"},
        {"bioassembly": operation([[0], [1]])},
    ],
)
def test_assembly_native_rejection_does_not_write(parameters):
    with msv.new_view(assembly_source()) as view:
        before = snapshot(view)
        with pytest.raises(Exception) as native:
            msm.build.make_bioassembly(view.molsys, **parameters)
        with pytest.raises(type(native.value)) as actual:
            view.addons.molsysmt.build.make_bioassembly(**parameters)
        assert str(actual.value) == str(native.value)
        unchanged(view, before)


@pytest.mark.parametrize(
    "problem",
    [
        "scheme",
        "hydrogen_parent",
        "unknown_inventory",
        "charge",
        "nan",
        "forcefield",
        "incomplete",
    ],
)
def test_projection_retains_native_chemistry_prerequisite_failures(problem):
    source = declared_methanol()
    kwargs = {"typing_scheme": "autodock4"}
    state = source.chemical_states._states[0]
    if problem == "scheme":
        kwargs["typing_scheme"] = "unknown"
    elif problem == "hydrogen_parent":
        kwargs["selection"] = [2]
    elif problem == "unknown_inventory":
        state.atom_attributes.loc[0, "n_explicit_hydrogens"] = None
    elif problem == "charge":
        state.atom_attributes.loc[2, "formal_charge"] = 1
    elif problem == "nan":
        source.molecular_mechanics.partial_charge = [np.nan] * 6
    elif problem == "forcefield":
        source.molecular_mechanics.forcefield = "unqualified_model"
    else:
        state.connectivity_completeness = "partial"
    with msv.new_view(source) as view:
        before = snapshot(view)
        with pytest.raises(Exception) as native:
            msm.build.merge_nonpolar_hydrogens(view.molsys, **kwargs)
        with pytest.raises(type(native.value)) as actual:
            view.addons.molsysmt.build.merge_nonpolar_hydrogens(**kwargs)
        assert str(actual.value) == str(native.value)
        unchanged(view, before)


def test_pending_reader_does_not_synchronize_or_adopt(case):
    name, view = case
    tools = view.addons.molsysmt
    coordinates = puw.get_value(view.molsys.structures.coordinates, to_unit="nm") + 2
    tools.basic.set(coordinates=puw.quantity(coordinates, "nm"), update_view=False)
    before = snapshot(view)
    actual = getattr(tools.build, name)(**parameters_for(name))
    native = getattr(msm.build, name)(view.molsys, **parameters_for(name))
    same(actual, native)
    assert tools.get_sync_status()["state"] == "pending"
    unchanged(view, before)


def test_cached_tools_rebind_and_reject_closed_empty_owners(case):
    name, view = case
    method = getattr(view.addons.molsysmt.build, name)
    replacement = source_for(name)
    values = puw.get_value(replacement.structures.coordinates, to_unit="nm") + 4
    msm.set(replacement, coordinates=puw.quantity(values, "nm"))
    view.load(replacement, mode="replace")
    before = snapshot(view)
    same(
        method(**parameters_for(name)),
        getattr(msm.build, name)(view.molsys, **parameters_for(name)),
    )
    unchanged(view, before)
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method(**parameters_for(name))
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt.build, name)(**parameters_for(name))
