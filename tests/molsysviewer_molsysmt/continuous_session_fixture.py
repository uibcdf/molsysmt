"""One continuous expert/GUI workflow with independent molecular oracles."""

import json
from copy import deepcopy
from pathlib import Path

import molsysviewer as msv
import numpy as np
import pytest
from molsysviewer.interactions import InteractionAnalysisError

import molsysmt as msm

# The launcher imports this fixture as a sibling script; kernels/pytest use
# the owning test package. Neither route may bind the sibling Viewer's tests.
if __package__:
    from .test_scientific_session import compare_molecular, xyz
else:
    from test_scientific_session import compare_molecular, xyz

puw = msm.pyunitwizard


def same_quantity(actual, expected):
    if expected is None:
        assert actual is None
    elif puw.is_quantity(expected):
        assert puw.is_quantity(actual)
        np.testing.assert_array_equal(
            puw.get_value(actual, to_unit=puw.get_unit(expected)),
            puw.get_value(expected),
        )
    else:
        np.testing.assert_array_equal(actual, expected)


def pairs(mapping):
    return [(s + i, t + i) for s, t, n in mapping["runs"] for i in range(n)]


class ContinuousSession:
    """Own all views, explicit source inputs and recovery references in one run."""

    def __init__(self, output):
        self.output = Path(output)
        self.output.mkdir(parents=True, exist_ok=True)
        self.owned = []
        self.checks = []

    def own(self, view):
        self.owned.append(view)
        return view

    def record(self, phase, **details):
        self.checks.append(dict(phase=phase, **details))
        (self.output / "scientific-ledger.json").write_text(
            json.dumps(self.checks, indent=2) + "\n"
        )

    def start(self):
        self.seed = self.own(msv.demo["pentalanine"])
        self.seed_molsys = self.seed.molsys
        self.tctim = self.own(msv.demo["1TCD"])
        self.protein = msm.copy(self.tctim.molsys)
        self.caffeine = msm.convert(
            msm.systems["caffeine"]["caffeine.sdf"], to_form="molsysmt.MolSys"
        )
        self.peptide = msm.extract(self.seed_molsys, structure_indices=[0])
        self.view = self.own(msv.MolSysView())
        self.view.load(
            [self.protein, self.caffeine], multiple=True, labels=["TcTIM", "Caffeine"]
        )
        self.view.load(self.peptide, label="Peptide")
        progressive = self.own(msv.MolSysView())
        for system, label in [
            (self.protein, "TcTIM"),
            (self.caffeine, "Caffeine"),
            (self.peptide, "Peptide"),
        ]:
            progressive.load(system, label=label)
        np.testing.assert_array_equal(xyz(self.view.molsys), xyz(progressive.molsys))
        assert len(self.view.load_blocks) == len(progressive.load_blocks) == 3
        assert len({r["source_id"] for r in self.view.load_blocks}) == 3
        for record, other, system in zip(
            self.view.load_blocks,
            progressive.load_blocks,
            [self.protein, self.caffeine, self.peptide],
            strict=True,
        ):
            assert record["atom_map"] == other["atom_map"]
            assert (
                self.view.regions[record["region_tag"]].atom_indices
                == progressive.regions[other["region_tag"]].atom_indices
            )
            for a, b in pairs(record["atom_map"]):
                np.testing.assert_array_equal(
                    xyz(self.view.molsys)[0, b], xyz(system)[0, a]
                )
        self.sources = deepcopy(self.view.load_blocks)
        same_quantity(self.view.molsys.structures.box, self.protein.structures.box)
        same_quantity(self.view.molsys.structures.time, self.protein.structures.time)
        complementary = self.own(
            msv.new_view(
                [
                    self.peptide.topology,
                    self.peptide.chemical_states,
                    self.peptide.structures,
                ]
            )
        )
        assert len(complementary.load_blocks) == 1 and not complementary.regions
        compare_molecular(self.peptide, complementary.molsys)
        paired_source = msm.extract(self.seed_molsys, structure_indices=[0, 8, 3])
        msm.set(paired_source, time=None)
        paired = self.own(msv.MolSysView())
        paired.load(
            [paired_source, paired_source],
            multiple=True,
            structure_indices=[[2, 0], [0, 2]],
            structure_pairing="by_index",
        )
        for record in paired.load_blocks:
            for s, t in pairs(record["structure_map"]):
                for a, b in pairs(record["atom_map"]):
                    np.testing.assert_array_equal(
                        xyz(paired.molsys)[t, b], xyz(paired_source)[s, a]
                    )
        assert paired.molsys.structures.time is None
        self.before_remove = msm.copy(self.view.molsys)
        self.removed = self.view.addons.molsysmt.basic.select(
            "group_type=='water' or group_type=='ion'"
        )
        assert len(self.removed) > 0
        self.keep = np.setdiff1d(
            np.arange(self.before_remove.get_n_atoms()), self.removed
        )
        self.record(
            "composed",
            atoms=self.view.molsys.get_n_atoms(),
            source_ids=[r["source_id"] for r in self.sources],
            first_box=self.protein.structures.box is not None,
            paired_time_absent=True,
        )
        return self.view

    def after_remove(self):
        compare_molecular(self.before_remove, self.before_remove.copy())
        np.testing.assert_array_equal(
            xyz(self.view.molsys), xyz(self.before_remove)[:, self.keep]
        )
        assert not len(
            self.view.addons.molsysmt.basic.select(
                "group_type=='water' or group_type=='ion'"
            )
        )
        assert [r["source_id"] for r in self.view.load_blocks] == [
            r["source_id"] for r in self.sources
        ]
        inverse = {int(old): new for new, old in enumerate(self.keep)}
        for old, current in zip(self.sources, self.view.load_blocks, strict=True):
            assert pairs(current["atom_map"]) == [
                (a, inverse[b]) for a, b in pairs(old["atom_map"]) if b in inverse
            ]
        self.after_removal = msm.copy(self.view.molsys)
        subset = self.own(self.view.extract(selection=[0, 2, 4]))
        np.testing.assert_array_equal(
            xyz(subset.molsys), xyz(self.view.molsys)[:, [0, 2, 4]]
        )
        permutation = msm.basic.permute_atoms(
            subset.molsys, [2, 0, 1], return_report=True
        )
        np.testing.assert_array_equal(
            permutation["report"]["output_to_source_atom_indices"], [2, 0, 1]
        )
        np.testing.assert_array_equal(
            xyz(permutation["molecular_system"]), xyz(subset.molsys)[:, [2, 0, 1]]
        )
        ordered = self.own(msv.new_view(permutation["molecular_system"]))
        ordered.addons.molsysmt.structure.translate(
            translation="[1,0,0] nm", in_place=True
        )
        compare_molecular(self.after_removal, self.view.molsys)
        copied = self.own(msv.tools.basic.copy(self.view))
        self.independent_copy = copied
        assert copied.load_blocks == self.view.load_blocks
        copied.addons.molsysmt.structure.translate(
            translation="[0,1,0] nm", in_place=True
        )
        compare_molecular(self.after_removal, self.view.molsys)
        self.independent_reference = msm.copy(copied.molsys)
        # Retire auxiliary Views once their exact source/map controls finish.
        # The source MolSys stays explicitly retained for subsequent selections.
        for auxiliary in self.owned:
            if auxiliary is not self.view and auxiliary is not copied:
                auxiliary.close()
        self.record(
            "removed_and_copied",
            removed=len(self.removed),
            retained=len(self.keep),
            explicit_order=[2, 0, 1],
        )

    def after_preparation(self):
        compare_molecular(self.after_removal, self.view.molsys)
        records = self.view.addons.manager.presentations.records()
        assert len(records) == 1
        child = self.view.addons.manager.presentations.get(records[0]["id"])
        assert child.molsys is not self.view.molsys
        assert child.molsys.get_n_atoms() > 0
        self.prepared = self.own(child)
        self.prepared_reference = msm.copy(child.molsys)
        self.prepared_data = child.molsys
        child.close()
        # Preparation is an independent result; it never replaces the composed source.
        self.record(
            "prepared_independent",
            result_atoms=child.molsys.get_n_atoms(),
            source_ids=[r["source_id"] for r in self.view.load_blocks],
        )
        tools = self.view.addons.molsysmt
        ca = tools.basic.select("atom_name=='CA'")
        assert len(ca) > 3
        original = xyz(self.view.molsys).copy()
        reference = msm.copy(self.view.molsys)
        box = deepcopy(self.view.molsys.structures.box)
        displacement = np.array([0.1, -0.2, 0.05])
        tools.structure.translate(
            selection=ca,
            translation="[100,-200,50] pm",
            in_place=True,
            update_view=False,
        )
        assert tools.get_sync_status()["state"] == "pending"
        np.testing.assert_allclose(
            xyz(self.view.molsys)[:, ca], original[:, ca] + displacement, atol=1e-13
        )
        revision = tools.get_sync_status()["target_revision"]
        tools.sync_view()
        assert tools.get_sync_status()["state"] == "synchronized"
        assert tools.get_sync_status()["target_revision"] == revision
        rmsd = tools.structure.get_rmsd(
            selection=ca,
            reference_molecular_system=reference,
            reference_selection=ca,
            reference_structure_index=0,
        )
        np.testing.assert_allclose(
            puw.get_value(rmsd, to_unit="nm"), np.linalg.norm(displacement), atol=1e-12
        )
        tools.structure.least_rmsd_fit(
            selection=ca,
            selection_fit=ca,
            reference_molecular_system=reference,
            reference_selection_fit=ca,
            reference_structure_index=0,
            in_place=True,
            use_gpu=False,
            precision="double",
        )
        np.testing.assert_allclose(
            xyz(self.view.molsys)[:, ca], original[:, ca], atol=1e-10
        )
        unselected = np.setdiff1d(np.arange(len(original[0])), ca)
        np.testing.assert_array_equal(
            xyz(self.view.molsys)[:, unselected], original[:, unselected]
        )
        same_quantity(self.view.molsys.structures.box, box)
        self.record(
            "transformed_and_fitted",
            ca_atoms=len(ca),
            displacement_nm=displacement.tolist(),
            deferred_revision=revision,
        )
        self.view.regions.add(selection=ca, tag="alpha-carbons")
        self.view.measurements.add_distance(
            [int(ca[0])], [int(ca[1])], tag="ca-distance"
        )
        self.view.annotations.add(
            "TcTIM reference fit", atom_indices=ca[:3], tag="reference-fit"
        )
        self.main_before_save = msm.copy(self.view.molsys)
        self.main_sources = deepcopy(self.view.load_blocks)
        self.ensemble = self.own(self.seed.extract(structure_indices=[0, 8, 3]))
        self.ensemble_before = xyz(self.ensemble.molsys).copy()
        expected = self.ensemble_before.copy()
        expected[[2, 0]] += [0.1, -0.2, 0.05]
        self.ensemble.addons.molsysmt.structure.translate(
            structure_indices=[2, 0], translation="[1,-2,.5] angstrom", in_place=True
        )
        np.testing.assert_allclose(xyz(self.ensemble.molsys), expected, atol=1e-14)
        self.ensemble_expected = expected
        with puw.context(standard_units=["pm", "ps"]):
            rg = self.ensemble.addons.molsysmt.structure.get_radius_of_gyration(
                selection="all", structure_indices=[2, 0]
            )
        coords = expected[[2, 0]]
        oracle = np.sqrt(
            np.mean(
                np.sum((coords - coords.mean(axis=1, keepdims=True)) ** 2, axis=-1),
                axis=1,
            )
        )
        np.testing.assert_allclose(
            puw.get_value(rg, to_unit="nm").reshape(-1), oracle, atol=1e-12
        )
        self.record(
            "ensemble_observed",
            source_structures=[0, 8, 3],
            local_query=[2, 0],
            gyration_nm=oracle.tolist(),
            distance_nm=np.linalg.norm(
                expected[[2, 0], 0] - expected[[2, 0], 2], axis=-1
            ).tolist(),
        )
        return self.ensemble

    def interactions(self):
        import faulthandler

        import psutil

        process = psutil.Process()

        def step(name):
            with (self.output / "interaction-steps.jsonl").open("a") as report:
                report.write(
                    json.dumps(
                        {"stage": name, "rss_mib": process.memory_info().rss / 2**20}
                    )
                    + "\n"
                )

        with (self.output / "interaction-stacks.log").open("w") as stack:
            faulthandler.dump_traceback_later(1, repeat=True, file=stack)
            try:
                tools = self.ensemble.addons.molsysmt
                step("before-initial-query")
                initial = tools.interactions.hbonds.get_buch_hbonds(
                    structure_indices=[2, 0],
                    pbc=False,
                    output_type="molsysmt.Interactions",
                )
                assert initial.n_interactions == 0
                self.ensemble.interactions.attach(
                    initial, name="initial-empty", assume_aligned=True
                )
                tools.h5msm.write(str(self.output / "initial-empty-system.h5msm"))
                self.record(
                    "native_empty_original_conformations",
                    source_structures=[0, 8, 3],
                    evaluated=initial.evaluated_structure_indices.tolist(),
                    occurrences=0,
                    replacement_source_structures=[0, 8, 2],
                    criterion_changed=False,
                )
                # Preserve the genuine empty result. Explicitly replace the sampled
                # conformations for a known positive control, never widen the criterion
                # or attach observations to coordinates on which they were not measured.
                step("before-replace")
                self.ensemble.load(
                    self.seed_molsys,
                    mode="replace",
                    structure_indices=[0, 8, 2],
                    label="Hbond conformations",
                )
                assert "initial-empty" not in self.ensemble.molsys.interactions
                step("after-replace")
                self.hbond_source_coordinates = xyz(self.ensemble.molsys).copy()
                self.ensemble.addons.molsysmt.structure.translate(
                    structure_indices=[2, 0],
                    translation="[1,-2,.5] angstrom",
                    in_place=True,
                )
                step("after-translation")
                self.ensemble_expected = self.hbond_source_coordinates.copy()
                self.ensemble_expected[[2, 0]] += [0.1, -0.2, 0.05]
                np.testing.assert_allclose(
                    xyz(self.ensemble.molsys), self.ensemble_expected, atol=1e-14
                )
                self.ensemble.measurements.add_distance(
                    [0], [2], tag="retained-distance"
                )
                tools = self.ensemble.addons.molsysmt
                step("before-positive-query")
                positive = tools.interactions.hbonds.get_buch_hbonds(
                    structure_indices=[2, 0],
                    pbc=False,
                    output_type="molsysmt.Interactions",
                )
                step("after-positive-query")
                assert positive.n_interactions > 0
                self.ensemble.interactions.attach(
                    positive, name="legacy-buch", assume_aligned=True
                )
                self.ensemble.interactions.add("legacy-buch", tag="hbonds")
                # A genuinely empty evaluated structure under the unchanged
                # default criterion. The tiny-cutoff resource defect is owned
                # separately by MolSysMT #690, not compensated in this addon.
                zero = tools.interactions.hbonds.get_buch_hbonds(
                    structure_indices=[0],
                    pbc=False,
                    output_type="molsysmt.Interactions",
                )
                assert zero.n_interactions == 0
                self.ensemble.interactions.attach(
                    zero, name="empty", assume_aligned=True
                )
                self.ensemble.interactions.add("empty", tag="empty")
                assert (
                    self.ensemble.interactions.inspect("empty", structure_index=0)[
                        "status"
                    ]
                    == "evaluated"
                )
                assert (
                    self.ensemble.interactions.inspect("empty", structure_index=1)[
                        "status"
                    ]
                    == "unevaluated"
                )
                step("before-visual-lifecycle")
                original = deepcopy(positive.to_dict())
                visual = self.ensemble.interactions["hbonds"]
                visual.hide()
                visual.show()
                visual.delete()
                np.testing.assert_equal(positive.to_dict(), original)
                assert (
                    self.ensemble.interactions.get_analysis("legacy-buch") is positive
                )
                self.ensemble.interactions.add("legacy-buch", tag="hbonds")
                step("before-analysis-save")
                self.ensemble.interactions.save(
                    self.output / "independent.h5msm", analysis_names=["legacy-buch"]
                )
                with pytest.raises(InteractionAnalysisError, match="align|correspond"):
                    self.ensemble.interactions.load(
                        self.output / "independent.h5msm",
                        analysis_name="legacy-buch",
                        name="imported",
                    )
                assert "imported" not in self.ensemble.molsys.interactions
                self.ensemble.interactions.load(
                    self.output / "independent.h5msm",
                    analysis_name="legacy-buch",
                    name="imported",
                    assume_aligned=True,
                )
                np.testing.assert_equal(
                    self.ensemble.interactions.get_analysis("imported").to_dict(),
                    original,
                )
                step("before-analysis-delete")
                self.ensemble.interactions.delete_analysis("imported")
                assert "legacy-buch" in self.ensemble.molsys.interactions
                step("before-visible-structure")
                self.ensemble.player.go_to_structure(2)
                for item in self.ensemble.interactions.inspect(
                    "hbonds", structure_index=2
                )["observations"]:
                    roles = {p["role"]: p["atom_indices"] for p in item["participants"]}
                    h, a = roles["hydrogen"][0], roles["acceptor"][0]
                    distance = np.linalg.norm(
                        self.ensemble_expected[2, h] - self.ensemble_expected[2, a]
                    )
                    np.testing.assert_allclose(
                        item["measurements"]["distance"], distance, atol=1e-12
                    )
                self.record(
                    "interactions",
                    method=positive.method,
                    occurrences=positive.n_interactions,
                    units=positive.measure_units,
                    evaluated=positive.evaluated_structure_indices.tolist(),
                    independent_correspondence_declared=True,
                )
            finally:
                faulthandler.cancel_dump_traceback_later()

    async def recover(self):
        for name, view in [("composed", self.view), ("ensemble", self.ensemble)]:
            native_path = self.output / (name + ".h5msm")
            view.addons.molsysmt.h5msm.write(str(native_path))
            compare_molecular(
                view.molsys, view.addons.molsysmt.h5msm.read(str(native_path))
            )
            path = self.output / (name + ".msv")
            await view.save_session_async(path)
            saved_scene = view.export_state()
            saved_data = msm.copy(view.molsys)
            sources = deepcopy(view.load_blocks)
            saved_structure = int(view.player.index)
            view.close()
            recovered = self.own(msv.load_session(path))
            compare_molecular(saved_data, recovered.molsys)
            # Closing retires transports, not the retained serializable comparison.
            assert recovered.export_state()["regions"] == saved_scene["regions"]
            for key in (
                "selections",
                "active_selection",
                "annotations",
                "measurements",
                "measurement_settings",
                "shapes",
                "whole",
                "interactions",
            ):
                assert recovered.export_state().get(key) == saved_scene.get(key), key
            assert recovered.load_blocks == sources
            assert recovered.player.index == saved_structure
            for analysis_name, analysis in saved_data.interactions.items():
                np.testing.assert_equal(
                    recovered.interactions.get_analysis(analysis_name).to_dict(),
                    analysis.to_dict(),
                )
            setattr(self, "recovered_" + name, recovered)
        self.record(
            "closed_and_recovered",
            scientific_and_scene=True,
            named_analyses=list(self.recovered_ensemble.molsys.interactions),
        )
        return self.recovered_ensemble

    def continue_after_recovery(self):
        view = self.recovered_ensemble
        before = xyz(view.molsys).copy()
        analysis = view.interactions.get_analysis("legacy-buch")
        observations = deepcopy(analysis.query().to_dict())
        records = deepcopy(view.load_blocks)
        target = view.molsys
        with pytest.raises(ValueError, match="explicit analysis merge"):
            view.load(view.molsys, mode="append_structures", structure_indices=[2, 0])
        assert view.molsys is target and view.load_blocks == records
        view.load(self.seed_molsys, mode="append_structures", structure_indices=[2, 0])
        np.testing.assert_array_equal(
            xyz(view.molsys),
            np.concatenate([before, self.hbond_source_coordinates[[2, 0]]]),
        )
        retained = view.interactions.get_analysis("legacy-buch")
        np.testing.assert_array_equal(
            retained.evaluated_structure_indices, analysis.evaluated_structure_indices
        )
        for key in ("occurrence_indices", "structure_indices", "relation_indices"):
            np.testing.assert_array_equal(
                retained.query().to_dict()[key], observations[key]
            )
        assert retained.n_structures == 5
        assert (
            view.interactions.inspect("hbonds", structure_index=4)["status"]
            == "unevaluated"
        )
        view.addons.molsysmt.structure.translate(
            structure_indices=[2], translation="[0,0,1] angstrom", in_place=True
        )
        np.testing.assert_array_equal(
            view.interactions.get_analysis("legacy-buch").evaluated_structure_indices,
            [0],
        )
        assert self.prepared.closed
        compare_molecular(self.prepared_reference, self.prepared_data)
        assert not self.independent_copy.closed
        compare_molecular(self.independent_reference, self.independent_copy.molsys)
        compare_molecular(self.main_before_save, self.recovered_composed.molsys)
        assert self.recovered_composed.load_blocks == self.main_sources
        self.record(
            "continued_after_recovery",
            structures=5,
            invalidated_only=[2],
            preserved_evaluated=[0],
            source_ids_retained=True,
        )
        return view

    def close(self):
        for view in reversed(self.owned):
            view.close()


def notebook_cells(prefix, output):
    return [
        prefix
        + f"from tests.molsysviewer_molsysmt.continuous_session_fixture import ContinuousSession\nsession=ContinuousSession({str(output)!r})\nview=session.start()\nview\n",
        "session.after_remove()\nprint('CONTINUOUS_REMOVAL_OK')\n",
        "ensemble=session.after_preparation()\nensemble\n",
        "session.interactions()\nprint('CONTINUOUS_INTERACTIONS_OK')\n",
        "recovered=await session.recover()\nrecovered\n",
        "session.continue_after_recovery()\nprint('CONTINUOUS_RECOVERY_OK')\n",
    ]
