"""Independent source receiving of a molecular work session and recovery."""

import inspect

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest

import molsysmt as msm

puw = msm.pyunitwizard
COMPONENT_STORAGE = [
    pytest.param(object, id="object"),
    pytest.param(pd.StringDtype(), id="nullable-string"),
]
# Only runtimes exposing this representation can produce the CI-observed
# NaN-backed string inventory. Older admitted pandas keep the other cases.
if "na_value" in inspect.signature(pd.StringDtype).parameters:
    COMPONENT_STORAGE.append(
        pytest.param(pd.StringDtype(na_value=np.nan), id="nan-string")
    )


def xyz(system):
    return puw.get_value(system.structures.coordinates, to_unit="nm")


def compare_molecular(before, after):
    assert after.get_n_atoms() == before.get_n_atoms()
    assert after.structures.n_structures == before.structures.n_structures
    for name in ("atoms", "groups", "molecules", "chains", "entities"):
        left, right = (
            getattr(before.topology, name).copy(),
            getattr(after.topology, name).copy(),
        )
        # The legacy demo has object IDs/None; H5MSM 0.5 canonicalizes
        # those same labels and missing values to nullable string columns.
        # Compare the full inventory with that declared normalization only.
        for column in left:
            if column.endswith("_id"):
                assert all(isinstance(value, str) for value in left[column].dropna())
                assert all(isinstance(value, str) for value in right[column].dropna())
                left[column], right[column] = (
                    left[column].astype("string"),
                    right[column].astype("string"),
                )
        pd.testing.assert_frame_equal(left, right)
    np.testing.assert_array_equal(xyz(after), xyz(before))
    for name in (
        "box",
        "time",
        "b_factor",
        "occupancy",
        "structure_id",
        "chemical_state_index",
    ):
        left, right = (
            getattr(before.structures, name, None),
            getattr(after.structures, name, None),
        )
        if puw.is_quantity(left):
            assert puw.is_quantity(right), name
            np.testing.assert_array_equal(
                puw.get_value(left), puw.get_value(right, to_unit=puw.get_unit(left))
            )
        else:
            np.testing.assert_equal(left, right, err_msg=name)
    a, b = before.chemical_states, after.chemical_states
    assert a.n_atoms == b.n_atoms
    assert a._reference_index == b._reference_index
    assert a.n_chemical_states == b.n_chemical_states
    for left, right in zip(a._states, b._states, strict=True):
        for key in (
            "state_id",
            "connectivity_completeness",
            "component_completeness",
            "component_evidence",
            "provenance_index",
        ):
            assert getattr(left, key) == getattr(right, key), key
        pd.testing.assert_series_equal(left.component_indices, right.component_indices)
        for field in ("components", "atom_attributes", "bonds"):
            x, y = getattr(left, field).copy(), getattr(right, field).copy()
            for column in x:
                # The format promises canonical nullable strings. Require
                # all source non-null values to be strings before allowing
                # that storage-only normalization; compare every value/null.
                if (
                    x[column].dtype == object
                    or isinstance(x[column].dtype, pd.StringDtype)
                ) and isinstance(y[column].dtype, pd.StringDtype):
                    assert all(isinstance(value, str) for value in x[column].dropna())
                    assert all(isinstance(value, str) for value in y[column].dropna())
                    np.testing.assert_array_equal(
                        x[column].isna().to_numpy(), y[column].isna().to_numpy()
                    )
                    canonical = pd.StringDtype(storage="python")
                    x[column] = x[column].astype(canonical)
                    y[column] = y[column].astype(canonical)
            pd.testing.assert_frame_equal(x, y)


def compare_scene(before, after):
    left, right = before.export_state(), after.export_state()
    for key in (
        "regions",
        "selections",
        "active_selection",
        "annotations",
        "measurements",
        "measurement_settings",
        "shapes",
        "whole",
        "interactions",
    ):
        assert left.get(key) == right.get(key), key
    assert after.player.index == before.player.index


@pytest.mark.parametrize("component_storage", COMPONENT_STORAGE)
@pytest.mark.parametrize("change", ["value", "null-mask"])
def test_recovery_comparison_rejects_changed_chemical_values_and_nulls(
    component_storage, change
):
    with msv.demo["dialanine"] as view:
        before = view.molsys.copy()
        table = before.chemical_states._states[0].components
        table["component_name"] = pd.Series(
            ["declared"] * len(table), dtype=component_storage
        )
        after = before.copy()
        changed = after.chemical_states._states[0].components
        changed.loc[0, "component_name"] = "different" if change == "value" else None
        with pytest.raises(AssertionError):
            compare_molecular(before, after)


@pytest.mark.parametrize("component_storage", COMPONENT_STORAGE)
def test_tctim_edit_transform_analyze_and_recover(tmp_path, component_storage):
    with msv.demo["1TCD"] as view:
        # Exercise real molecular values under the supported source string
        # backings, before taking the scientific/workflow snapshot.
        components = view.molsys.chemical_states._states[0].components
        for column in ("component_name", "component_type"):
            components[column] = components[column].astype(component_storage)
        tools = view.addons.molsysmt
        initial = xyz(view.molsys).copy()
        n_initial = view.molsys.get_n_atoms()
        removed = tools.basic.select("group_type=='water' or group_type=='ion'")
        assert len(removed) > 0
        keep = np.setdiff1d(np.arange(n_initial), removed)
        view.regions.add(selection=[0, 2, 4], tag="original-site")
        tools.basic.remove(selection=removed, in_place=True)
        np.testing.assert_array_equal(xyz(view.molsys), initial[:, keep])
        assert tools.get_sync_status()["state"] == "synchronized"
        ca = tools.basic.select("atom_name=='CA'")
        reference = view.molsys.copy()
        translated = xyz(reference).copy()
        displacement = np.array([0.1, -0.2, 0.05])
        translated[:, ca] += displacement
        tools.structure.translate(
            selection=ca, translation="[1, -2, 0.5] angstrom", in_place=True
        )
        np.testing.assert_allclose(xyz(view.molsys), translated, atol=1e-14)
        rmsd = tools.structure.get_rmsd(
            selection=ca,
            reference_molecular_system=reference,
            reference_selection=ca,
            reference_structure_index=0,
        )
        np.testing.assert_allclose(
            puw.get_value(rmsd, to_unit="nm"), np.linalg.norm(displacement), atol=1e-12
        )
        coordinates = xyz(view.molsys)[:, ca]
        rg_expected = np.sqrt(
            np.mean(
                np.sum(
                    (coordinates - coordinates.mean(axis=1, keepdims=True)) ** 2,
                    axis=-1,
                ),
                axis=1,
            )
        )
        with puw.context(standard_units=["pm", "ps"]):
            rg = tools.structure.get_radius_of_gyration(selection=ca)
        np.testing.assert_allclose(
            puw.get_value(rg, to_unit="nm"), rg_expected, atol=1e-12
        )
        view.regions.add(selection=ca, tag="alpha-carbons")
        view.selections.add("chosen-ca", atom_indices=ca[:3])
        view.active_selection.set(ca[:3])
        view.annotations.add(
            "Reviewed alpha carbons", atom_indices=ca[:3], tag="review"
        )
        view.measurements.add_distance([int(ca[0])], [int(ca[1])], tag="ca-distance")
        data_path = str(tmp_path / "tctim-edited.h5msm")
        tools.h5msm.write(data_path)
        compare_molecular(view.molsys, tools.h5msm.read(data_path))
        session = tmp_path / "tctim-edited.msv"
        view.save_session(session)
        with msv.load_session(session) as recovered:
            compare_molecular(view.molsys, recovered.molsys)
            compare_scene(view, recovered)
            recovered.addons.molsysmt.structure.translate(
                translation="[0, 0, 1] angstrom", in_place=True
            )
            np.testing.assert_allclose(xyz(view.molsys), translated, atol=1e-14)


def test_ensemble_interactions_and_nonconsecutive_recovery(tmp_path):
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 2]) as view:
            tools = view.addons.molsysmt
            original = xyz(view.molsys).copy()
            tools.structure.translate(
                selection="all",
                structure_indices=[2, 0],
                translation="[1, -2, 0.5] angstrom",
                in_place=True,
            )
            expected = original.copy()
            expected[[2, 0]] += [0.1, -0.2, 0.05]
            np.testing.assert_allclose(xyz(view.molsys), expected, atol=1e-14)
            analysis = tools.interactions.hbonds.get_buch_hbonds(
                structure_indices=[2, 0], pbc=False, output_type="molsysmt.Interactions"
            )
            assert analysis.n_interactions > 0
            assert analysis.query(structure_indices=[0]).n_interactions == 0
            view.interactions.attach(
                analysis, name="hydrogen-bonds", assume_aligned=True
            )
            view.interactions.add("hydrogen-bonds", tag="hbonds")
            empty = view.interactions.inspect("hbonds", structure_index=0)
            assert empty["status"] == "evaluated" and empty["total"] == 0
            assert (
                view.interactions.inspect("hbonds", structure_index=1)["status"]
                == "unevaluated"
            )
            view.player.go_to_structure(2)
            inspection = view.interactions.inspect("hbonds", structure_index=2)
            assert inspection["observations"]
            for observation in inspection["observations"]:
                roles = {
                    p["role"]: p["atom_indices"] for p in observation["participants"]
                }
                assert all(
                    len(roles[role]) == 1 for role in ("donor", "hydrogen", "acceptor")
                )
                h, a = roles["hydrogen"][0], roles["acceptor"][0]
                distance = np.linalg.norm(expected[2, h] - expected[2, a])
                assert distance <= 0.23
                np.testing.assert_allclose(
                    observation["measurements"]["distance"], distance, atol=1e-12
                )
            view.regions.add(selection=[0, 2], tag="translated")
            view.measurements.add_distance([0], [2], tag="distance")
            path = tmp_path / "ensemble.msv"
            view.save_session(path)
            with msv.load_session(path) as recovered:
                compare_molecular(view.molsys, recovered.molsys)
                compare_scene(view, recovered)
                left = view.interactions.get_analysis("hydrogen-bonds")
                right = recovered.interactions.get_analysis("hydrogen-bonds")
                np.testing.assert_equal(left.to_dict(), right.to_dict())
                np.testing.assert_array_equal(
                    left.query().to_dict()["occurrence_indices"],
                    right.query().to_dict()["occurrence_indices"],
                )
                np.testing.assert_array_equal(
                    left.occurrence_structures, right.occurrence_structures
                )
                np.testing.assert_array_equal(
                    left.participant_atoms, right.participant_atoms
                )
                np.testing.assert_array_equal(
                    left.evaluated_structure_indices, right.evaluated_structure_indices
                )
                assert set(right.evaluated_structure_indices) == {0, 2}
                assert left.parameters == right.parameters
                assert left.measure_units == right.measure_units
                assert left.method == right.method
                for key, values in left.measurements.items():
                    np.testing.assert_array_equal(values, right.measurements[key])
