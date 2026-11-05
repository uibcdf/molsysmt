"""Receive independent peptide construction and bounded native substitutions."""

import inspect

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import UnassessedResidueWarning
from molsysmt.native import Structures
from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
    same,
    snapshot,
    unchanged,
)

puw = msm.pyunitwizard
NAMES = ("mutate", "build_peptide")


def source(*, heavy=False, multiple=False):
    result = msm.build.build_peptide("AlaValPro", engine="MolSysMT")
    if heavy:
        result = msm.remove(result, selection="atom_type=='H'")
    xyz = puw.get_value(result.structures.coordinates, to_unit="nm")
    count = 3 if multiple else 1
    result.structures = Structures(
        coordinates=puw.quantity(
            np.concatenate([xyz + 3 * i for i in range(count)]), "nm"
        ),
        time=puw.quantity([2, 7, 15][:count], "ps"),
        box=puw.quantity(np.tile(5 * np.eye(3), (count, 1, 1)), "nm"),
        structure_id=[11, 24, 80][:count],
    )
    result.interactions = {
        "saved": msm.Interactions.from_records(
            [],
            n_atoms=result.get_n_atoms(),
            n_structures=count,
            evaluated_structure_indices=list(range(count)),
            method="receiving.sequence",
        )
    }
    return result


def parameters(name):
    return dict(mutations={1: "GLY"}) if name == "mutate" else {}


@pytest.fixture(params=NAMES)
def case(request):
    with msv.new_view(source()) as view:
        view.regions.add(selection=[0], tag="keep")
        view.shapes.add_sphere(atom_indices=[0], tag="anchor")
        yield request.param, view


def test_native_scientific_signature_help_namespace_and_local_skip(case):
    name, view = case
    method = getattr(view.addons.molsysmt.build, name)
    native = inspect.signature(getattr(msm.build, name))
    expected = list(native.parameters.values())[1:] + [
        inspect.Parameter(
            "skip_digestion", inspect.Parameter.KEYWORD_ONLY, default=False
        )
    ]
    assert inspect.signature(method) == native.replace(parameters=expected)
    assert method.digestion_plan is not None and name in dir(view.addons.molsysmt.build)
    assert not hasattr(view.addons.molsysmt, name)
    doc = inspect.getdoc(method)
    assert "separate molecular system" in doc and "no update_view" in doc
    assert "\nmolecular_system :" not in doc
    for parameter in inspect.signature(method).parameters:
        assert f"{parameter} :" in doc
    for key in (
        "molecular_system",
        "in_place",
        "update_view",
        "structure_indices",
        "prepare",
    ):
        with pytest.raises(UnknownArgumentError):
            method(**parameters(name), **{key: None})
    with pytest.raises(Exception):
        method(**parameters(name), skip_digestion="yes")


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("skip", [False, True])
def test_build_peptide_constructs_one_new_geometry_from_current_sequence(unit, skip):
    molsys = source(multiple=True)
    molsys.structures.coordinates = molsys.structures.coordinates + puw.quantity(
        20, "nm"
    )
    with msv.new_view(molsys) as view:
        before = snapshot(view)
        with puw.context(standard_units=[unit, "ps"]):
            output = view.addons.molsysmt.build.build_peptide(skip_digestion=skip)
            expected = msm.build.build_peptide(view.molsys)
        assert output is not view.molsys
        assert msm.get(output, element="group", group_name=True) == [
            "ALA",
            "VAL",
            "PRO",
        ]
        assert output.get_n_atoms() == 40 and output.structures.n_structures == 1
        assert output.structures.box is None and not output.interactions
        xyz = puw.get_value(output.structures.coordinates, to_unit="nm")[0]
        assert np.isfinite(xyz).all() and np.max(np.abs(xyz)) < 5
        pairs = msm.get(output, bonded_atom_pairs=True)
        lengths = np.linalg.norm(
            xyz[np.array(pairs)[:, 0]] - xyz[np.array(pairs)[:, 1]], axis=1
        )
        assert np.all((lengths > 0.09) & (lengths < 0.185))
        same(output, expected)
        unchanged(view, before)


@pytest.mark.parametrize("to_form", ["mdtraj.Trajectory", "string:amino_acids_3"])
def test_build_peptide_explicit_native_output_forms(to_form):
    with msv.new_view(source()) as view:
        before = snapshot(view)
        output = view.addons.molsysmt.build.build_peptide(to_form=to_form)
        assert msm.get_form(output) == to_form
        if to_form == "mdtraj.Trajectory":
            assert (output.n_frames, output.n_atoms) == (1, 40)
            np.testing.assert_allclose(
                output.xyz, msm.build.build_peptide(view.molsys, to_form=to_form).xyz
            )
        else:
            assert output.lower() == "alavalpro"
        unchanged(view, before)


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize(
    "args",
    [
        dict(mutations={1: "GLY"}),
        dict(mutations={"1": "GLY"}, keys="group_id"),
        dict(mutations={"VAL": "GLY"}, keys="group_name"),
        dict(mutations=["VAL-1-GLY"]),
    ],
)
def test_native_mutation_specifications_keep_backbone_and_source(args, unit):
    with msv.new_view(source()) as view:
        before = snapshot(view)
        with puw.context(standard_units=[unit, "ps"]):
            output = view.addons.molsysmt.build.mutate(**args)
        assert output is not view.molsys and output.get_n_atoms() == 31
        assert msm.get(output, element="group", group_name=True) == [
            "ALA",
            "GLY",
            "PRO",
        ]
        assert msm.build.get_missing_heavy_atoms(output) == {}
        assert set(
            msm.get(
                output, selection="group_index==1 and atom_type!='H'", atom_name=True
            )
        ) == {"N", "CA", "C", "O"}
        for group in (0, 1, 2):
            selected = f"group_index=={group}" + (
                " and atom_type!='H'" if group == 1 else ""
            )
            if group == 1:
                selected += " and atom_name in ['N','CA','C','O']"
            np.testing.assert_array_equal(
                puw.get_value(
                    msm.get(output, selection=selected, coordinates=True), to_unit="nm"
                ),
                puw.get_value(
                    msm.get(view.molsys, selection=selected, coordinates=True),
                    to_unit="nm",
                ),
            )
        same(output, msm.build.mutate(view.molsys, **args))
        unchanged(view, before)


def test_heavy_only_mutation_retains_all_structures_axes_and_observed_coordinates():
    with msv.new_view(source(heavy=True, multiple=True)) as view:
        before = snapshot(view)
        output = view.addons.molsysmt.build.mutate(mutations={1: "GLY"})
        assert output.structures.n_structures == 3
        assert not msm.select(output, selection="atom_type=='H'")
        assert output.structures.structure_id.tolist() == [11, 24, 80]
        np.testing.assert_array_equal(
            puw.get_value(output.structures.time, to_unit="ps"), [2, 7, 15]
        )
        mapping = pd.Index(view.molsys.topology.atoms.atom_id).get_indexer(
            output.topology.atoms.atom_id
        )
        assert (mapping >= 0).all()
        np.testing.assert_array_equal(
            puw.get_value(output.structures.coordinates, to_unit="nm"),
            puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[:, mapping],
        )
        np.testing.assert_array_equal(
            puw.get_value(output.structures.box, to_unit="nm"),
            puw.get_value(view.molsys.structures.box, to_unit="nm"),
        )
        same(output, msm.build.mutate(view.molsys, mutations={1: "GLY"}))
        unchanged(view, before)


def test_unsupported_native_sidechain_is_reported_incomplete_without_fallback():
    with msv.new_view(source()) as view:
        before = snapshot(view)
        with pytest.warns(UnassessedResidueWarning, match="TRP.*multiple missing"):
            output = view.addons.molsysmt.build.mutate(mutations={1: "TRP"})
        assert output.get_n_atoms() == 30
        assert msm.build.get_missing_heavy_atoms(output) == {
            1: ["CB", "CD1", "CD2", "CE2", "CE3", "CG", "CH2", "CZ2", "CZ3", "NE1"]
        }
        unchanged(view, before)


def test_explicit_pdbfixer_mutation_receives_inventory_without_pose_certificate():
    with msv.new_view(source(heavy=True)) as view:
        before = snapshot(view)
        output = view.addons.molsysmt.build.mutate(
            mutations={1: "TRP"}, engine="PDBFixer"
        )
        names = msm.get(
            output, selection="group_index==1 and atom_type!='H'", atom_name=True
        )
        assert {
            "CB",
            "CG",
            "CD1",
            "CD2",
            "NE1",
            "CE2",
            "CE3",
            "CZ2",
            "CZ3",
            "CH2",
        } <= set(names)
        assert msm.get(output, element="group", group_name=True) == [
            "ALA",
            "TRP",
            "PRO",
        ]
        unchanged(view, before)


@pytest.mark.parametrize(
    "syntax,selection", [("MolSysMT", "group_index==1"), ("MDTraj", "resid 1")]
)
@pytest.mark.parametrize("skip", [False, True])
def test_mutation_mask_syntax_and_local_skip_remain_native(syntax, selection, skip):
    with msv.new_view(source()) as view:
        before = snapshot(view)
        args = dict(
            mutations={"VAL": "GLY"},
            keys="group_name",
            selection=selection,
            syntax=syntax,
        )
        if syntax == "MDTraj":
            # Native mutate does not yet forward its mask's external syntax.
            with pytest.raises(Exception, match="MolSysMT.*syntax") as native:
                msm.build.mutate(view.molsys, **args)
            with pytest.raises(type(native.value)) as actual:
                view.addons.molsysmt.build.mutate(**args, skip_digestion=skip)
            assert str(actual.value) == str(native.value)
        else:
            actual = view.addons.molsysmt.build.mutate(**args, skip_digestion=skip)
            same(actual, msm.build.mutate(view.molsys, **args))
            assert msm.get(actual, element="group", group_name=True) == [
                "ALA",
                "GLY",
                "PRO",
            ]
        unchanged(view, before)


def test_native_atom_mask_axis_rejection_is_preserved_without_consumer_reinterpretation():
    with msv.new_view(source()) as view:
        before = snapshot(view)
        atoms = msm.select(view.molsys, selection="group_index==1")
        args = dict(mutations={"VAL": "GLY"}, keys="group_name", selection=atoms)
        with pytest.raises(Exception, match="out-of-range group indices") as native:
            msm.build.mutate(view.molsys, **args)
        with pytest.raises(type(native.value)) as actual:
            view.addons.molsysmt.build.mutate(**args)
        assert str(actual.value) == str(native.value)
        unchanged(view, before)


@pytest.mark.parametrize("skip", [False, True])
def test_native_failure_is_not_bypassed_by_local_skip(case, skip):
    name, view = case
    before = snapshot(view)
    args = parameters(name) | dict(engine="unavailable")
    with pytest.raises(Exception) as expected:
        getattr(msm.build, name)(view.molsys, **args)
    with pytest.raises(type(expected.value)) as actual:
        getattr(view.addons.molsysmt.build, name)(**args, skip_digestion=skip)
    assert str(actual.value) == str(expected.value)
    unchanged(view, before)


def test_pending_reader_does_not_synchronize_or_adopt(case):
    name, view = case
    tools = view.addons.molsysmt
    tools.basic.set(coordinates=view.molsys.structures.coordinates, update_view=False)
    before = snapshot(view)
    same(
        getattr(tools.build, name)(**parameters(name)),
        getattr(msm.build, name)(view.molsys, **parameters(name)),
    )
    assert tools.get_sync_status()["state"] == "pending"
    unchanged(view, before)


def test_cached_tool_reads_replacement_and_rejects_closed_empty_owners(case):
    name, view = case
    method = getattr(view.addons.molsysmt.build, name)
    replacement = source(heavy=True)
    replacement.structures.coordinates = (
        replacement.structures.coordinates + puw.quantity(2, "nm")
    )
    view.load(replacement, mode="replace")
    before = snapshot(view)
    same(
        method(**parameters(name)),
        getattr(msm.build, name)(view.molsys, **parameters(name)),
    )
    unchanged(view, before)
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method(**parameters(name))
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt.build, name)(**parameters(name))
