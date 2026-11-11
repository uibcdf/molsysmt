"""Receive explicit H-generation modes and native terminal preparation."""

import inspect

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import StructuralAttributeDropWarning
from molsysmt.native import Structures
from tests.build.add_missing_hydrogens.test_fixed_state import prepared
from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
    same,
    snapshot,
    unchanged,
)
from tests.native.test_preparation_history import assert_tree

puw = msm.pyunitwizard
NAMES = ("add_missing_hydrogens", "add_missing_terminal_cappings")
FIXED = dict(pH=None, engine="RDKit", mode="fixed_chemical_state")


def source_for(name):
    if name == "add_missing_hydrogens":
        return prepared("CO", [[0, 0, 0], [1.4, 0, 0]])
    return msm.build.build_peptide("AlaValPro", engine="MolSysMT")


def parameters_for(name):
    return (
        FIXED.copy()
        if name == "add_missing_hydrogens"
        else dict(N_terminal="ACE", C_terminal="NME")
    )


@pytest.fixture(params=NAMES)
def case(request):
    name = request.param
    with msv.new_view(source_for(name)) as view:
        view.regions.add(selection=[0], tag="keep")
        view.shapes.add_sphere(atom_indices=[0], tag="anchor")
        yield name, view


def test_explicit_native_signature_help_and_validation(case):
    name, view = case
    method = getattr(view.addons.molsysmt.build, name)
    native = inspect.signature(getattr(msm.build, name))
    assert inspect.signature(method) == native.replace(
        parameters=list(native.parameters.values())[1:]
    )
    assert method.digestion_plan is not None and name in dir(view.addons.molsysmt.build)
    assert not hasattr(view.addons.molsysmt, name)
    doc = inspect.getdoc(method)
    assert "separate molecular system" in doc and "no update_view control" in doc
    assert "\nmolecular_system :" not in doc
    for parameter in inspect.signature(method).parameters:
        assert f"{parameter} :" in doc
    for key in ("molecular_system", "update_view", "in_place", "prepare"):
        with pytest.raises(UnknownArgumentError):
            method(**parameters_for(name), **{key: None})
    with pytest.raises(Exception):
        method(**parameters_for(name), skip_digestion="yes")


@pytest.mark.parametrize(
    "name", ["add_missing_heavy_atoms", "add_missing_terminal_cappings"]
)
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_reconstruction_reports_are_forwarded_once_without_adoption(
    monkeypatch, name, unit
):
    from tests.build.add_missing_heavy_atoms.test_domain_preservation import (
        incomplete_serine,
    )

    source = (
        incomplete_serine() if name == "add_missing_heavy_atoms" else source_for(name)
    )
    parameters = {} if name == "add_missing_heavy_atoms" else parameters_for(name)
    native = getattr(msm.build, name)
    calls, results = [], []

    def receive(molecular_system, **options):
        calls.append(options.copy())
        result = native(molecular_system, **options)
        results.append(result)
        return result

    with msv.new_view(source) as view:
        method = getattr(view.addons.molsysmt.build, name)
        before = snapshot(view)
        monkeypatch.setattr(msm.build, name, receive)
        with puw.context(standard_units=[unit, "ps", "radians", "elementary_charge"]):
            result = method(
                **parameters, attribute_policy="intersection", return_report=True
            )
        assert len(results) == 1 and result is results[0]
        assert calls[0]["return_report"] is True
        assert calls[0]["attribute_policy"] == "intersection"
        output, report = result["molecular_system"], result["report"]
        assert output is not view.molsys
        mapping = report["source_to_output_atom_indices"]
        inverse = report["output_to_source_atom_indices"]
        retained = np.flatnonzero(mapping >= 0)
        np.testing.assert_array_equal(inverse[mapping[retained]], retained)
        np.testing.assert_array_equal(
            puw.get_value(output.structures.coordinates, to_unit="nm")[
                :, mapping[retained]
            ],
            puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[
                :, retained
            ],
        )
        unchanged(view, before)


@pytest.mark.parametrize(
    "smiles,positions,count",
    [
        ("C", [[0, 0, 0]], 4),
        ("CO", [[0, 0, 0], [1.4, 0, 0]], 4),
        ("[NH4+]", [[0, 0, 0]], 4),
        ("CS", [[0, 0, 0], [1.8, 0, 0]], 4),
    ],
)
@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("return_report", [False, True])
def test_fixed_hydrogens_keep_pose_inventory_maps_units_and_source(
    smiles, positions, count, unit, return_report
):
    with msv.new_view(prepared(smiles, positions)) as view:
        source = view.molsys
        source.interactions = {
            "saved": msm.Interactions.from_records(
                [],
                n_atoms=source.get_n_atoms(),
                n_structures=1,
                evaluated_structure_indices=[0],
                method="receiving.fixed-H",
            )
        }
        before = snapshot(view)
        with puw.context(standard_units=[unit, "ps", "coulomb"]):
            result = view.addons.molsysmt.build.add_missing_hydrogens(
                **FIXED, return_report=return_report
            )
        output = result["molecular_system"] if return_report else result
        history = output.chemical_states.get_preparation_history()
        report = result["report"] if return_report else history[-1]["report"]
        n = source.get_n_atoms()
        assert output is not source and output.get_n_atoms() == n + count
        assert report["schema"] == "molsysmt.hydrogen_addition@1"
        assert report["coordinate_unit"] == "nm"
        assert report["coordinate_evidence"] == "generated_local_geometry"
        assert report["parameters"]["pH"] is None
        assert report["n_added_hydrogens"] == count
        np.testing.assert_array_equal(
            report["atom_correspondence"], np.column_stack((np.arange(n), np.arange(n)))
        )
        assert [r["report"]["schema"] for r in history] == [
            "molsysmt.terminal_attachment@1",
            "molsysmt.hydrogen_addition@1",
        ]
        np.testing.assert_array_equal(
            puw.get_value(output.structures.coordinates, to_unit="nm")[:, :n],
            puw.get_value(source.structures.coordinates, to_unit="nm"),
        )
        xyz = puw.get_value(output.structures.coordinates, to_unit="angstrom")[0]
        for parent, h in report["parent_hydrogen_pairs"]:
            low, high = {
                "C": (1.0, 1.15),
                "N": (0.95, 1.1),
                "O": (0.9, 1.05),
                "S": (1.25, 1.45),
            }[source.topology.atoms.at[parent, "atom_type"]]
            assert low < np.linalg.norm(xyz[h] - xyz[parent]) < high
        inventory = msm.physchem.get_hydrogen_inventory(output)
        assert inventory["missing_hydrogen_counts"].tolist() == [0] * (n + count)
        assert output.interactions["saved"].evaluated_structure_indices.size == 0
        assert (
            output.interactions["saved"].atom_source_indices.tolist()
            == list(range(n)) + [-1] * count
        )
        unchanged(view, before)


@pytest.mark.parametrize(
    "state,structures,skip",
    [("reference", "all", False), (0, [0], True), ("structure", 0, False)],
)
def test_fixed_state_structure_and_skip_choices_are_native(state, structures, skip):
    source = source_for("add_missing_hydrogens")
    source._structure_chemical_state_indices = np.array([0], dtype=np.int64)
    with msv.new_view(source) as view:
        before = snapshot(view)
        params = dict(
            **FIXED,
            chemical_state=state,
            structure_indices=structures,
            return_report=True,
            skip_digestion=skip,
        )
        actual = view.addons.molsysmt.build.add_missing_hydrogens(**params)
        expected = msm.build.add_missing_hydrogens(view.molsys, **params)
        same(actual, expected)
        unchanged(view, before)


def test_methane_geometry_and_no_addition_history_survive_h5msm(tmp_path):
    with msv.new_view(prepared("C", [[1.2, -0.7, 2.3]])) as view:
        source = view.molsys
        result = view.addons.molsysmt.build.add_missing_hydrogens(
            **FIXED, return_report=True
        )
        output, report = result["molecular_system"], result["report"]
        xyz = puw.get_value(output.structures.coordinates, to_unit="nm")[0]
        vectors = xyz[1:] - xyz[0]
        cosines = (
            vectors
            @ vectors.T
            / np.outer(np.linalg.norm(vectors, axis=1), np.linalg.norm(vectors, axis=1))
        )
        np.testing.assert_allclose(cosines[np.triu_indices(4, 1)], -1 / 3, atol=0.015)
        history = output.chemical_states.get_preparation_history()
        report["parent_hydrogen_pairs"][:] = -1
        assert_tree(output.chemical_states.get_preparation_history(), history)
        path = tmp_path / "fixed-H.h5msm"
        msm.convert(output, to_form=path)
        loaded = msm.convert(path, to_form="molsysmt.MolSys")
        assert_tree(loaded.chemical_states.get_preparation_history(), history)
        assert view.molsys is source and source.get_n_atoms() == 1
    with msv.new_view(loaded) as view:
        view.molsys.interactions = {
            "saved": msm.Interactions.from_records(
                [],
                n_atoms=5,
                n_structures=1,
                evaluated_structure_indices=[0],
                method="receiving.no-addition",
            )
        }
        before = snapshot(view)
        result = view.addons.molsysmt.build.add_missing_hydrogens(
            **FIXED, return_report=True
        )
        assert result["report"]["status"] == "unchanged"
        assert result["report"]["n_added_hydrogens"] == 0
        assert result["molecular_system"].interactions[
            "saved"
        ].evaluated_structure_indices.tolist() == [0]
        unchanged(view, before)


@pytest.mark.parametrize(
    "problem",
    ["pH", "engine", "mode", "state", "structure", "states", "strict", "disconnected"],
)
def test_fixed_native_rejection_preserves_source(problem):
    source = (
        prepared("C.C", [[0, 0, 0], [3, 0, 0]])
        if problem == "disconnected"
        else source_for("add_missing_hydrogens")
    )
    params = dict(**FIXED, return_report=True)
    if problem == "pH":
        params["pH"] = 7.4
    elif problem == "engine":
        params["engine"] = "OpenMM"
    elif problem == "mode":
        params["mode"] = "unknown"
    elif problem == "state":
        params["chemical_state"] = 8
    elif problem == "structure":
        params["structure_indices"] = [1]
    elif problem == "states":
        source.chemical_states._append_state(source.chemical_states._states[0].copy())
    elif problem == "strict":
        source.structures.occupancy = np.ones((1, source.get_n_atoms()))
        params["attribute_policy"] = "strict"
    with msv.new_view(source) as view:
        before = snapshot(view)
        with pytest.raises(Exception) as expected:
            msm.build.add_missing_hydrogens(view.molsys, **params)
        with pytest.raises(type(expected.value)) as actual:
            view.addons.molsysmt.build.add_missing_hydrogens(**params)
        assert str(actual.value) == str(expected.value)
        unchanged(view, before)


@pytest.mark.parametrize("engine", ["OpenMM", "PDBFixer", "MolSysMT"])
def test_legacy_single_structure_engines_keep_source_and_add_hydrogens(engine):
    source = msm.convert(msm.systems["Met-enkephalin"]["met_enkephalin.pdb"])
    source = msm.remove(source, selection="atom_type=='H'")
    with msv.new_view(source) as view:
        before = snapshot(view)
        output = view.addons.molsysmt.build.add_missing_hydrogens(pH=7.4, engine=engine)
        assert output is not view.molsys
        assert msm.select(output, selection="atom_type=='H'")
        assert not msm.select(view.molsys, selection="atom_type=='H'")
        assert (
            msm.get(output, selection="atom_type!='H'", n_atoms=True)
            == view.molsys.get_n_atoms()
        )
        unchanged(view, before)


@pytest.mark.parametrize(
    "ncap,ccap,groups,added",
    [
        (None, None, ["ALA", "VAL", "PRO"], 3),
        ("ACE", None, ["ACE", "ALA", "VAL", "PRO"], 7),
        (None, "NME", ["ALA", "VAL", "PRO", "NME"], 8),
        ("ACE", "NME", ["ACE", "ALA", "VAL", "PRO", "NME"], 12),
    ],
)
@pytest.mark.parametrize("skip", [False, True])
def test_terminal_completion_and_capping_preserve_native_group_order(
    ncap, ccap, groups, added, skip
):
    with msv.new_view(source_for("add_missing_terminal_cappings")) as view:
        before = snapshot(view)
        with pytest.warns(StructuralAttributeDropWarning):
            output = view.addons.molsysmt.build.add_missing_terminal_cappings(
                N_terminal=ncap, C_terminal=ccap, skip_digestion=skip
            )
        assert output is not view.molsys
        assert output.get_n_atoms() == view.molsys.get_n_atoms() + added
        assert msm.get(output, element="group", group_name=True) == groups
        # Native preparation also completes the opposite uncapped terminus.
        if ccap is None:
            assert "OXT" in output.topology.atoms.atom_name.tolist()
        if ncap is None:
            first = output.topology.atoms.loc[output.topology.atoms.group_index.eq(0)]
            assert {"H2", "H3"} <= set(first.atom_name)
        mapping = pd.Index(output.topology.atoms.atom_id).get_indexer(
            view.molsys.topology.atoms.atom_id
        )
        assert (mapping >= 0).all()
        np.testing.assert_array_equal(
            puw.get_value(output.structures.coordinates, to_unit="nm")[:, mapping],
            puw.get_value(view.molsys.structures.coordinates, to_unit="nm"),
        )
        unchanged(view, before)


def test_caps_cover_all_structures_and_invalidate_only_output_analysis():
    source = source_for("add_missing_terminal_cappings")
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm")
    source.structures = Structures(
        coordinates=puw.quantity(np.concatenate([xyz, xyz + 1]), "nm"),
        time=puw.quantity([3, 9], "ps"),
        structure_id=["A", "B"],
    )
    source.interactions = {
        "saved": msm.Interactions.from_records(
            [],
            n_atoms=source.get_n_atoms(),
            n_structures=2,
            evaluated_structure_indices=[0, 1],
            method="receiving.caps",
        )
    }
    with msv.new_view(source) as view:
        before = snapshot(view)
        with puw.context(standard_units=["pm", "fs"]):
            with pytest.warns(StructuralAttributeDropWarning):
                output = view.addons.molsysmt.build.add_missing_terminal_cappings(
                    N_terminal="ACE", C_terminal="NME"
                )
        assert output.structures.n_structures == 2
        np.testing.assert_array_equal(
            puw.get_value(output.structures.time, to_unit="ps"), [3, 9]
        )
        assert output.structures.structure_id.tolist() == ["A", "B"]
        assert output.interactions["saved"].evaluated_structure_indices.size == 0
        unchanged(view, before)


@pytest.mark.parametrize("engine,keep_ids", [("unknown", False), ("PDBFixer", True)])
def test_native_capping_engine_rejections_preserve_source(engine, keep_ids):
    with msv.new_view(source_for("add_missing_terminal_cappings")) as view:
        before = snapshot(view)
        params = dict(
            N_terminal="ACE", C_terminal="NME", engine=engine, keep_ids=keep_ids
        )
        with pytest.raises(Exception) as expected:
            msm.build.add_missing_terminal_cappings(view.molsys, **params)
        with pytest.raises(type(expected.value)) as actual:
            view.addons.molsysmt.build.add_missing_terminal_cappings(**params)
        assert str(actual.value) == str(expected.value)
        unchanged(view, before)


def test_pending_reads_do_not_sync_or_adopt(case):
    name, view = case
    tools = view.addons.molsysmt
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm") + 1
    tools.basic.set(coordinates=puw.quantity(xyz, "nm"), update_view=False)
    before = snapshot(view)
    actual = getattr(tools.build, name)(**parameters_for(name))
    expected = getattr(msm.build, name)(view.molsys, **parameters_for(name))
    same(actual, expected)
    assert tools.get_sync_status()["state"] == "pending"
    unchanged(view, before)


def test_cached_tools_rebind_and_reject_closed_empty_owners(case):
    name, view = case
    method = getattr(view.addons.molsysmt.build, name)
    source = source_for(name)
    msm.set(
        source,
        coordinates=puw.quantity(
            puw.get_value(source.structures.coordinates, to_unit="nm") + 2, "nm"
        ),
    )
    view.load(source, mode="replace")
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


@pytest.mark.parametrize("indices", ["all", [0]])
def test_fixed_generation_requires_extracting_a_single_structure_first(indices):
    source = source_for("add_missing_hydrogens")
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm")
    source.structures = Structures(
        coordinates=puw.quantity(np.concatenate([xyz, xyz + 1]), "nm")
    )
    with msv.new_view(source) as view:
        before = snapshot(view)
        with pytest.raises(Exception, match="one structure") as expected:
            msm.build.add_missing_hydrogens(
                view.molsys, **FIXED, structure_indices=indices
            )
        with pytest.raises(type(expected.value), match="one structure"):
            view.addons.molsysmt.build.add_missing_hydrogens(
                **FIXED, structure_indices=indices
            )
        unchanged(view, before)
