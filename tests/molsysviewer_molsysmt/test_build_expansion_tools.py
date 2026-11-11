"""Receive explicit terminal attachment and bounded native heavy-atom repair."""

import inspect
from copy import deepcopy

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import (
    StructuralAttributeDropWarning,
    UnassessedResidueWarning,
)
from tests.build.add_missing_heavy_atoms.test_domain_preservation import (
    incomplete_serine,
)
from tests.build.add_missing_heavy_atoms.test_modified_residues import (
    CASES,
    _incomplete_residue,
)
from tests.build.add_terminal_atoms.test_add_terminal_atoms import system
from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
    same,
    snapshot,
    unchanged,
)
from tests.native.test_preparation_history import assert_tree

puw = msm.pyunitwizard
NAMES = ("add_terminal_atoms", "add_missing_heavy_atoms")


def source_for(name):
    return system() if name == "add_terminal_atoms" else incomplete_serine()


def parameters_for(name):
    if name == "add_terminal_atoms":
        return {
            "new_atoms": [{"parent_atom_index": 1, "atom_type": "H", "atom_id": 40}],
            "coordinates": puw.quantity([[[0.14, 0, 0.1]], [[0.14, 0, 1.1]]], "nm"),
        }
    return {}


@pytest.fixture(params=NAMES)
def case(request):
    name = request.param
    with msv.new_view(source_for(name)) as view:
        view.regions.add(selection=[0], tag="keep")
        view.shapes.add_sphere(atom_indices=[0], tag="anchor")
        yield name, view


def test_native_signature_help_validation_and_ownership_controls(case):
    name, view = case
    method = getattr(view.addons.molsysmt.build, name)
    native = inspect.signature(getattr(msm.build, name))
    assert inspect.signature(method) == native.replace(
        parameters=list(native.parameters.values())[1:]
    )
    assert method.digestion_plan is not None
    assert name in dir(view.addons.molsysmt.build)
    assert not hasattr(view.addons.molsysmt, name)
    doc = inspect.getdoc(method)
    assert "separate molecular system" in doc and "no update_view control" in doc
    assert "\nmolecular_system :" not in doc
    for parameter in inspect.signature(method).parameters:
        assert f"{parameter} :" in doc
    for extra in (
        "molecular_system",
        "in_place",
        "update_view",
        "structure_indices",
    ):
        with pytest.raises(UnknownArgumentError):
            method(**parameters_for(name), **{extra: None})
    if name == "add_terminal_atoms":
        with pytest.raises(UnknownArgumentError):
            method(**parameters_for(name), return_report=None)
    with pytest.raises(Exception):
        method(**parameters_for(name), skip_digestion="yes")


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("skip", [False, True])
def test_terminal_supplied_geometry_identity_chemistry_report_and_source(unit, skip):
    with msv.new_view(system()) as view:
        source = view.molsys
        source.chemical_states._states[0].state_id = "explicit-state"
        source.chemical_states._states[0].provenance_index = 7
        source.interactions = {
            "saved": msm.Interactions.from_records(
                [],
                n_atoms=2,
                n_structures=2,
                evaluated_structure_indices=[0, 1],
                method="receiving.attachment",
            )
        }
        before = snapshot(view)
        records = [
            {
                "parent_atom_index": 1,
                "atom_type": "H",
                "atom_name": "D",
                "atom_id": 40,
                "isotope": 2,
                "bond_order": 1,
                "chemical_attributes": {"formal_charge": 0},
            }
        ]
        records_before = deepcopy(records)
        expected = np.array([[[0.14, 0, 0.1]], [[0.14, 0, 1.1]]])
        positions = puw.convert(puw.quantity(expected, "nm"), to_unit=unit)
        with puw.context(standard_units=[unit, "ps", "radians"]):
            result = view.addons.molsysmt.build.add_terminal_atoms(
                records,
                positions,
                skip_digestion=skip,
            )
        output, report = result["molecular_system"], result["report"]
        assert output is not source and output.get_n_atoms() == 3
        pd.testing.assert_frame_equal(
            output.topology.atoms.iloc[:2], source.topology.atoms
        )
        assert output.topology.atoms.atom_id.tolist() == ["10", "11", "40"]
        assert output.topology.atoms.loc[2, "isotope"] == 2
        assert (
            output.topology.atoms.loc[2, "group_index"]
            == source.topology.atoms.loc[1, "group_index"]
        )
        np.testing.assert_array_equal(
            puw.get_value(output.structures.coordinates, to_unit="nm")[:, :2],
            puw.get_value(source.structures.coordinates, to_unit="nm"),
        )
        np.testing.assert_allclose(
            puw.get_value(output.structures.coordinates, to_unit="nm")[:, 2:],
            expected,
            rtol=0,
            atol=1e-15,
        )
        state = output.chemical_states._states[0]
        assert state.state_id == "explicit-state" and state.provenance_index == 7
        assert state.atom_attributes.loc[2, "formal_charge"] == 0
        bonds = state.bonds
        assert ((bonds.atom1_index == 1) & (bonds.atom2_index == 2)).any()
        assert report["schema"] == "molsysmt.terminal_attachment@1"
        assert report["coordinate_unit"] == "nm"
        assert report["coordinate_evidence"] == "supplied_coordinates"
        assert report["source"] == {
            "n_atoms": 2,
            "n_structures": 2,
            "chemical_state_index": 0,
        }
        np.testing.assert_array_equal(report["atom_correspondence"], [[0, 0], [1, 1]])
        np.testing.assert_array_equal(report["parent_atom_pairs"], [[1, 2]])
        np.testing.assert_array_equal(report["structure_indices"], [0, 1])
        assert report["generated_atom_ids"] == ["40"]
        assert report["invalidated_interactions"] == ["saved"]
        assert report["software"]["molsysmt"] == msm.__version__
        saved = output.interactions["saved"]
        assert saved.n_atoms == 3 and saved.evaluated_structure_indices.size == 0
        assert saved.atom_source_indices.tolist() == [0, 1, -1]
        assert records == records_before
        unchanged(view, before)


@pytest.mark.parametrize("policy", ["intersection", "strict"])
@pytest.mark.parametrize("attribute", ["occupancy", "b_factor"])
def test_terminal_attribute_loss_or_strict_rejection_preserves_source(
    policy, attribute
):
    with msv.new_view(system()) as view:
        setattr(view.molsys.structures, attribute, np.ones((2, 2)))
        before = snapshot(view)
        if policy == "strict":
            with pytest.raises(Exception, match=attribute):
                view.addons.molsysmt.build.add_terminal_atoms(
                    **parameters_for("add_terminal_atoms"),
                    attribute_policy=policy,
                )
        else:
            with pytest.warns(StructuralAttributeDropWarning, match=attribute):
                result = view.addons.molsysmt.build.add_terminal_atoms(
                    **parameters_for("add_terminal_atoms"),
                    attribute_policy=policy,
                )
            assert result["report"]["dropped_attributes"] == [attribute]
            assert getattr(result["molecular_system"].structures, attribute) is None
        assert getattr(view.molsys.structures, attribute).shape == (2, 2)
        unchanged(view, before)


def test_empty_terminal_addition_preserves_coverage_and_detaches_history(tmp_path):
    with msv.new_view(system()) as view:
        source = view.molsys
        source.structures.occupancy = np.ones((2, 2))
        source.interactions = {
            "saved": msm.Interactions.from_records(
                [],
                n_atoms=2,
                n_structures=2,
                evaluated_structure_indices=[0, 1],
                method="receiving.empty-attachment",
            )
        }
        before = snapshot(view)
        result = view.addons.molsysmt.build.add_terminal_atoms(
            [],
            puw.quantity(np.empty((2, 0, 3)), "nm"),
            attribute_policy="strict",
        )
        output, report = result["molecular_system"], result["report"]
        assert output is not source and report["status"] == "unchanged"
        assert report["parent_atom_pairs"].shape == (0, 2)
        assert report["parent_atom_pairs"].dtype == np.int64
        assert output.interactions["saved"].evaluated_structure_indices.tolist() == [
            0,
            1,
        ]
        np.testing.assert_array_equal(
            output.structures.occupancy, source.structures.occupancy
        )
        history = output.chemical_states.get_preparation_history()
        assert history[-1]["report"]["coordinate_unit"] == "nm"
        report["source"]["n_atoms"] = 999
        assert (
            output.chemical_states.get_preparation_history()[-1]["report"]["source"][
                "n_atoms"
            ]
            == 2
        )
        path = tmp_path / "empty-attachment.h5msm"
        msm.convert(output, to_form="file:h5msm", output_filename=str(path))
        loaded = msm.convert(path, to_form="molsysmt.MolSys")
        assert_tree(loaded.chemical_states.get_preparation_history(), history)
        unchanged(view, before)


@pytest.mark.parametrize(
    "problem",
    [
        "out_of_bounds",
        "boolean_parent",
        "bad_element",
        "duplicate_id",
        "isotope",
        "bond_order",
        "frames",
        "nan",
        "units",
        "states",
    ],
)
def test_terminal_native_rejection_is_transactional(problem):
    source = system()
    params = parameters_for("add_terminal_atoms")
    record = params["new_atoms"][0]
    if problem == "out_of_bounds":
        record["parent_atom_index"] = 2
    elif problem == "boolean_parent":
        record["parent_atom_index"] = True
    elif problem == "bad_element":
        record["atom_type"] = "Du"
    elif problem == "duplicate_id":
        record["atom_id"] = "10"
    elif problem == "isotope":
        record["isotope"] = -1
    elif problem == "bond_order":
        record["bond_order"] = 1.0
    elif problem == "frames":
        params["coordinates"] = puw.quantity(np.zeros((1, 1, 3)), "nm")
    elif problem == "nan":
        params["coordinates"] = puw.quantity(np.full((2, 1, 3), np.nan), "nm")
    elif problem == "units":
        params["coordinates"] = puw.quantity(np.ones((2, 1, 3)), "ps")
    else:
        source.chemical_states._append_state(source.chemical_states._states[0].copy())
    with msv.new_view(source) as view:
        before = snapshot(view)
        with pytest.raises(Exception) as expected:
            msm.build.add_terminal_atoms(view.molsys, **params)
        with pytest.raises(type(expected.value)) as actual:
            view.addons.molsysmt.build.add_terminal_atoms(**params)
        assert str(actual.value) == str(expected.value)
        unchanged(view, before)


@pytest.mark.parametrize(
    "selection,syntax",
    [
        ("all", "MolSysMT"),
        ([0], "MolSysMT"),
        ("group_name=='SER'", "MolSysMT"),
        ("resname SER", "MDTraj"),
    ],
)
@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("skip", [False, True])
def test_heavy_repair_retains_ids_chemistry_observed_geometry_and_source(
    selection, syntax, unit, skip
):
    with msv.new_view(incomplete_serine()) as view:
        source = view.molsys
        before = snapshot(view)
        original_ids = source.topology.atoms.atom_id.tolist()
        with puw.context(standard_units=[unit, "ps", "radians"]):
            with pytest.warns(StructuralAttributeDropWarning, match="atoms_ff"):
                output = view.addons.molsysmt.build.add_missing_heavy_atoms(
                    selection=selection,
                    syntax=syntax,
                    skip_digestion=skip,
                )
        assert output is not source and output.get_n_atoms() == source.get_n_atoms() + 1
        mapping = pd.Index(output.topology.atoms.atom_id).get_indexer(original_ids)
        assert np.all(mapping >= 0) and output.topology.atoms.atom_id.is_unique
        np.testing.assert_array_equal(
            puw.get_value(output.structures.coordinates, to_unit="nm")[:, mapping],
            puw.get_value(source.structures.coordinates, to_unit="nm"),
        )
        old, new = source.chemical_states._states[0], output.chemical_states._states[0]
        assert (
            new.state_id == old.state_id
            and new.provenance_index == old.provenance_index
        )
        pd.testing.assert_frame_equal(
            new.atom_attributes.iloc[mapping].reset_index(drop=True),
            old.atom_attributes,
        )
        added = output.topology.atoms.index[
            ~output.topology.atoms.atom_id.isin(original_ids)
        ]
        assert output.topology.atoms.loc[added, "atom_name"].tolist() == ["OG"]
        assert new.atom_attributes.loc[added].isna().all().all()
        saved = output.interactions["declared-analysis"]
        assert (
            saved.method == "independent-control"
            and saved.occurrence_structures.size == 0
        )
        assert saved.evaluated_structure_indices.size == 0
        np.testing.assert_array_equal(
            saved.atom_source_indices[mapping], np.arange(len(mapping))
        )
        np.testing.assert_array_equal(saved.participant_atoms, mapping[[0, -1]])
        assert saved.atom_source_indices[added].tolist() == [-1]
        np.testing.assert_array_equal(output._structure_chemical_state_indices, [0])
        unchanged(view, before)


@pytest.mark.parametrize("case_data", CASES, ids=[x[0] for x in CASES])
def test_curated_modified_heavy_repair_matches_observed_structure(case_data):
    missing = case_data[4]
    source, observed = _incomplete_residue(
        case_data, {missing}, ideal=case_data[0] == "SEP"
    )
    with msv.new_view(source) as view:
        before = snapshot(view)
        output = view.addons.molsysmt.build.add_missing_heavy_atoms()
        selected = output.topology.atoms.index[
            output.topology.atoms.atom_name.eq(missing)
        ]
        assert len(selected) == 1
        assert output.topology.atoms.loc[selected[0], "atom_type"] == case_data[5]
        xyz = puw.get_value(output.structures.coordinates, to_unit="nm")[0, selected[0]]
        assert np.linalg.norm(xyz - observed[missing][1]) < 0.05
        unchanged(view, before)


@pytest.mark.parametrize(
    "variant", ["collinear", "nonfinite", "wrong_element", "duplicate"]
)
def test_unassessed_heavy_atoms_are_not_fabricated(variant):
    with msv.new_view(incomplete_serine()) as view:
        source = view.molsys
        if variant == "collinear":
            source.structures.coordinates = puw.quantity(
                np.arange(source.get_n_atoms() * 3).reshape(1, -1, 3), "nm"
            )
        elif variant == "nonfinite":
            xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
            xyz[0, 0, 0] = np.nan
            source.structures.coordinates = puw.quantity(xyz, "nm")
        elif variant == "wrong_element":
            source.topology.atoms.loc[
                source.topology.atoms.atom_name.eq("CB"), "atom_type"
            ] = "Na"
        else:
            source.topology.atoms.at[0, "atom_name"] = "CA"
        before = snapshot(view)
        with pytest.warns(UnassessedResidueWarning):
            output = view.addons.molsysmt.build.add_missing_heavy_atoms()
        assert output.get_n_atoms() == source.get_n_atoms()
        pd.testing.assert_frame_equal(output.topology.atoms, source.topology.atoms)
        unchanged(view, before)


@pytest.mark.parametrize("problem", ["strict", "states", "engine", "PDBFixer_strict"])
def test_heavy_native_rejection_preserves_source(problem):
    source = incomplete_serine()
    params = {}
    if problem == "strict":
        params["attribute_policy"] = "strict"
    elif problem == "states":
        source.chemical_states._append_state(source.chemical_states._states[0].copy())
    elif problem == "engine":
        params["engine"] = "unsupported"
    else:
        params.update(engine="PDBFixer", attribute_policy="strict")
    with msv.new_view(source) as view:
        before = snapshot(view)
        with pytest.raises(Exception) as expected:
            msm.build.add_missing_heavy_atoms(view.molsys, **params)
        with pytest.raises(type(expected.value)) as actual:
            view.addons.molsysmt.build.add_missing_heavy_atoms(**params)
        assert str(actual.value) == str(expected.value)
        unchanged(view, before)


def test_heavy_explicit_optional_engine_and_selection():
    with msv.new_view(incomplete_serine()) as view:
        before = snapshot(view)
        actual = view.addons.molsysmt.build.add_missing_heavy_atoms(
            engine="PDBFixer", selection=[0]
        )
        expected = msm.build.add_missing_heavy_atoms(
            view.molsys, engine="PDBFixer", selection=[0]
        )
        same(actual, expected)
        assert actual.get_n_atoms() == view.molsys.get_n_atoms() + 1
        unchanged(view, before)


def test_pending_reads_never_synchronize_or_adopt(case):
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


def test_cached_methods_rebind_and_reject_closed_or_empty(case):
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


@pytest.mark.parametrize("unit", ["angstrom", "pm"])
def test_heavy_repair_covers_every_structure_and_preserves_time_box_and_ids(unit):
    from molsysmt.native import Structures

    source = incomplete_serine()
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm")
    # Rebuild this fixture's domains before declaring the new three-frame scope.
    source.interactions = {}
    source._structure_chemical_state_indices = None
    source.structures = Structures(
        coordinates=puw.quantity(np.concatenate([xyz, xyz + 1, xyz - 2]), "nm"),
        box=puw.quantity(np.repeat((np.eye(3) * 4)[None], 3, axis=0), "nm"),
        time=puw.quantity([5, 10, 30], "ps"),
        structure_id=["first", "middle", "last"],
    )
    source._structure_chemical_state_indices = np.zeros(3, dtype=np.int64)
    source.interactions = {
        "saved": msm.Interactions.from_records(
            [],
            n_atoms=source.get_n_atoms(),
            n_structures=3,
            evaluated_structure_indices=[0, 2],
            method="receiving.ensemble-repair",
        )
    }
    with msv.new_view(source) as view:
        before = snapshot(view)
        with puw.context(standard_units=[unit, "fs", "radians"]):
            with pytest.warns(StructuralAttributeDropWarning):
                output = view.addons.molsysmt.build.add_missing_heavy_atoms()
        mapping = pd.Index(output.topology.atoms.atom_id).get_indexer(
            view.molsys.topology.atoms.atom_id
        )
        np.testing.assert_array_equal(
            puw.get_value(output.structures.coordinates, to_unit="nm")[:, mapping],
            puw.get_value(view.molsys.structures.coordinates, to_unit="nm"),
        )
        og = output.topology.atoms.index[output.topology.atoms.atom_name.eq("OG")][0]
        positions = puw.get_value(output.structures.coordinates, to_unit="nm")[:, og]
        np.testing.assert_allclose(
            positions - positions[0],
            [[0, 0, 0], [1, 1, 1], [-2, -2, -2]],
            rtol=0,
            atol=1e-14,
        )
        np.testing.assert_array_equal(
            puw.get_value(output.structures.time, to_unit="ps"), [5, 10, 30]
        )
        np.testing.assert_array_equal(
            puw.get_value(output.structures.box, to_unit="nm"),
            puw.get_value(view.molsys.structures.box, to_unit="nm"),
        )
        assert output.structures.structure_id.tolist() == ["first", "middle", "last"]
        np.testing.assert_array_equal(
            output._structure_chemical_state_indices, [0, 0, 0]
        )
        assert output.interactions["saved"].evaluated_structure_indices.size == 0
        unchanged(view, before)


def test_empty_heavy_selection_returns_independent_unchanged_analysis_snapshot():
    with msv.new_view(incomplete_serine()) as view:
        before = snapshot(view)
        output = view.addons.molsysmt.build.add_missing_heavy_atoms(selection=[])
        assert output is not view.molsys
        same(output, view.molsys)
        assert output.interactions[
            "declared-analysis"
        ].evaluated_structure_indices.tolist() == [0]
        unchanged(view, before)


def test_terminal_nonempty_history_and_maps_survive_h5msm_without_adoption(tmp_path):
    with msv.new_view(system()) as view:
        before = snapshot(view)
        result = view.addons.molsysmt.build.add_terminal_atoms(
            **parameters_for("add_terminal_atoms")
        )
        output, report = result["molecular_system"], result["report"]
        history = output.chemical_states.get_preparation_history()
        assert history[-1]["report"]["schema"] == "molsysmt.terminal_attachment@1"
        np.testing.assert_array_equal(
            history[-1]["report"]["parent_atom_pairs"], [[1, 2]]
        )
        report["parent_atom_pairs"][:] = -1
        np.testing.assert_array_equal(
            output.chemical_states.get_preparation_history()[-1]["report"][
                "parent_atom_pairs"
            ],
            [[1, 2]],
        )
        path = tmp_path / "terminal-attachment.h5msm"
        msm.convert(output, to_form="file:h5msm", output_filename=str(path))
        loaded = msm.convert(path, to_form="molsysmt.MolSys")
        assert loaded.get_n_atoms() == 3
        assert_tree(loaded.chemical_states.get_preparation_history(), history)
        np.testing.assert_array_equal(
            puw.get_value(loaded.structures.coordinates, to_unit="nm"),
            puw.get_value(output.structures.coordinates, to_unit="nm"),
        )
        unchanged(view, before)
