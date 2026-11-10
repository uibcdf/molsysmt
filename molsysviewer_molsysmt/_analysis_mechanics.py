"""Reviewed native mechanical readings with explicit source and unit axes."""

from dataclasses import dataclass
from secrets import token_urlsafe
from weakref import ref

import numpy as np

from ._mechanical_review import _mechanical_model
from ._task_panel import _structures

MECHANICAL_METHODS = {
    "potential_energy": "get_potential_energy",
    "energy_terms": "get_potential_energy",
    "forces": "get_forces",
    "mechanical_dof": "get_degrees_of_freedom",
}
WHOLE_MECHANICAL_TASKS = set(MECHANICAL_METHODS) - {"forces"}
MECHANICAL_DEFAULTS = {"mechanical_platform": "Reference", "force_output": "components"}


def validate_mechanical_parameters(p):
    if not isinstance(p["mechanical_platform"], str) or p[
        "mechanical_platform"
    ] not in {"CPU", "Reference"}:
        raise ValueError("Choose CPU or Reference for this received mechanical route.")
    if not isinstance(p["force_output"], str) or p["force_output"] not in {
        "components",
        "magnitude",
    }:
        raise ValueError("Choose explicit atomic force components or magnitude.")


@dataclass(frozen=True)
class _MechanicalReview:
    token: str
    target: object
    revision: int
    frame: int
    parameters: dict
    first_draft: dict
    second_draft: dict
    atoms: np.ndarray
    frames: list
    model: tuple


class _MechanicalReports:
    def _prepare_mechanical_review(self, target):
        status = self._owner.get_sync_status()
        p = self._parameters
        if p["task"] not in MECHANICAL_METHODS or status["state"] not in {
            "synchronized",
            "pending",
            "sync_failed",
        }:
            raise ValueError("Choose a mechanical task with available molecular data.")
        atoms = (
            self._population(target, self._draft, status)
            if p["task"] == "forces"
            else np.arange(int(target.get_n_atoms()), dtype=np.int64)
        )
        frames = _structures(
            p["structures"],
            p["indices"],
            int(target.structures.n_structures),
            int(self._view.player.index),
            allow_repeated=True,
        )
        if p["task"] != "forces" and len(frames) != 1:
            raise ValueError(
                "This native energy/model reader receives one explicit structure. Choose Current structure or one index; no hidden trajectory loop is performed."
            )
        model = _mechanical_model(target, purpose="mechanical analysis")
        return _MechanicalReview(
            token_urlsafe(18),
            ref(target),
            status["target_revision"],
            int(self._view.player.index),
            dict(p),
            dict(self._draft),
            dict(self._second),
            atoms,
            frames,
            model,
        )

    def _current_mechanical_review(self, context):
        review = self._mechanics_review
        if review is None:
            return None
        if (
            self._view.molsys is not review.target()
            or context.get("target_revision") != review.revision
            or context.get("state") not in {"synchronized", "pending", "sync_failed"}
            or (review.parameters, review.first_draft, review.second_draft)
            != (self._parameters, self._draft, self._second)
            or (
                (
                    review.parameters["structures"] == "current"
                    or (
                        review.parameters["task"] == "forces"
                        and review.first_draft["context"] == "current"
                    )
                )
                and context.get("structure_index") != review.frame
            )
        ):
            self._mechanics_review = None
            return None
        return review

    def _mechanical_review_summary(self, context):
        review = self._current_mechanical_review(context)
        if review is None:
            return None
        return dict(
            token=review.token,
            source_revision=review.revision,
            atom_count=len(review.atoms),
            structure_indices=review.frames[:200],
            structure_count=len(review.frames),
            structures_truncated=len(review.frames) > 200,
            engine="OpenMM",
            platform=review.parameters["mechanical_platform"],
            model=[
                dict(name=k, value=v, unit=u, source=s) for k, v, u, s in review.model
            ],
        )

    def _take_mechanical_review(self, payload):
        review = self._current_mechanical_review(self._context())
        if (
            review is None
            or not isinstance(payload.get("review_token"), str)
            or payload["review_token"] != review.token
        ):
            raise ValueError(
                "Review the current mechanical model before calculating. Changed inputs or source data require a new review."
            )
        return review

    def _calculate_mechanical(self, target, status, review):
        import molsysmt as msm

        if (
            review is None
            or target is not review.target()
            or status["target_revision"] != review.revision
        ):
            raise ValueError(
                "This mechanical review no longer belongs to the current source."
            )
        current = self._prepare_mechanical_review(target)
        if (
            current.model != review.model
            or current.frames != review.frames
            or not np.array_equal(current.atoms, review.atoms)
            or current.parameters != review.parameters
            or current.first_draft != review.first_draft
            or current.second_draft != review.second_draft
        ):
            raise ValueError(
                "The model, source population or calculation settings changed. Review them again before calculation."
            )
        p, task = self._parameters, self._parameters["task"]
        frames, atoms = review.frames, review.atoms
        metadata = dict(
            model=review.model,
            platform=p["mechanical_platform"],
            engine="OpenMM",
        )
        if task == "forces":
            native = self._owner.molecular_mechanics.get_forces(
                selection=atoms.tolist(),
                structure_indices=frames,
                magnitude=p["force_output"] == "magnitude",
                platform=p["mechanical_platform"],
                engine="OpenMM",
            )
            values = np.asarray(
                msm.pyunitwizard.get_value(native, to_unit="kJ/(mol*nm)"), dtype=float
            )
            expected = (len(frames), len(atoms)) + (
                () if p["force_output"] == "magnitude" else (3,)
            )
            if values.shape != expected or not np.all(np.isfinite(values)):
                raise ValueError(
                    "Native forces do not match the finite source structure/atom axes."
                )
            unit, layout, total = (
                "kJ/(mol*nm)",
                "mechanical_forces",
                len(frames) * len(atoms),
            )
            metadata["notice"] = (
                "Forces are evaluated in the complete molecular environment; the atom selection filters returned values only. No minimization, integration, force aggregation or parameter assignment is applied to the source."
            )
        else:
            # The legacy energy/model tools have no public frame argument. A
            # deliberately requested single-structure native projection avoids
            # evaluating frame zero or hiding a loop across the trajectory.
            projected = msm.extract(target, structure_indices=frames)
            reader = getattr(msm.molecular_mechanics, MECHANICAL_METHODS[task])
            if task == "mechanical_dof":
                fields = {name: value for name, value, _, _ in review.model}
                native = reader(
                    projected,
                    forcefield=fields["forcefield"],
                    water_model=fields["water_model"],
                    implicit_solvent=fields["implicit_solvent"],
                )
                values, unit = np.asarray([int(native)]), "dimensionless"
                metadata["terms"] = ["3 × engine particles − engine constraints"]
                metadata["notice"] = (
                    "Native mechanical count, including engine particles and constraints. No center-of-mass, thermal or virtual-site correction is inferred. This is not a thermodynamic degrees-of-freedom estimate."
                )
            else:
                native = reader(
                    projected,
                    selection="all",
                    decomposition=task == "energy_terms",
                    platform=p["mechanical_platform"],
                    engine="OpenMM",
                )
                terms = (
                    native
                    if isinstance(native, dict)
                    else {"Total potential energy": native}
                )
                metadata["terms"] = list(terms)
                values = np.asarray(
                    [
                        float(msm.pyunitwizard.get_value(v, to_unit="kJ/mol"))
                        for v in terms.values()
                    ]
                )
                unit = "kJ/mol"
                metadata["notice"] = (
                    "Complete-model potential energy for one explicitly selected structure. Decomposition retains native force-class terms, not atom/group contributions. No preparation, integration, minimization or engine fallback is inferred."
                )
            if values.ndim != 1 or not np.all(np.isfinite(values)):
                raise ValueError(
                    "Native mechanical values must be finite on the declared term axis."
                )
            layout, total = "mechanical_terms", len(values)
        # Observe provenance only after the public native reader has enforced
        # its dependency boundary and completed successfully.
        import openmm

        metadata["openmm"] = str(openmm.__version__)
        return self._report_type(
            token=token_urlsafe(18),
            target=ref(target),
            revision=status["target_revision"],
            visible_frame=int(self._view.player.index),
            first_draft=dict(self._draft),
            second_draft=dict(self._second),
            parameters=dict(p),
            frames=frames,
            first=atoms,
            second=np.empty(0, dtype=np.int64),
            selections=(False, False),
            values=values,
            native_values=native,
            unit=unit,
            auxiliary=metadata,
            offsets=None,
            layout=layout,
            total=total,
            periodic=False,
            software=str(msm.__version__)[:200],
        )

    def _mechanical_summary(self):
        r, m = self._report, self._report.auxiliary
        return dict(
            id=r.token,
            method="molsysmt.molecular_mechanics."
            + MECHANICAL_METHODS[r.parameters["task"]],
            software={"molsysmt": r.software, "openmm": m["openmm"]},
            rows=r.total,
            unit=r.unit,
            first_atoms=len(r.first),
            second_atoms=0,
            structure_indices=r.frames[:200],
            structures_truncated=len(r.frames) > 200,
            structure_count=len(r.frames),
            source_revision=r.revision,
            family="mechanical",
            result_axis="atom" if r.layout == "mechanical_forces" else "term",
            definition="Stored model requests and named native defaults, reviewed before calculation; broader effective-recipe work remains #582.",
            notice=m["notice"],
            engine=m["engine"],
            platform=m["platform"],
            mechanical_model=[
                dict(name=k, value=v, unit=u, source=s) for k, v, u, s in m["model"]
            ],
            periodic=None,
            requested_pbc=None,
            disk_backed=False,
            live_distance_unavailable="This mechanical result is not a pair distance.",
            plot_unavailable="Use an explicit compatible mechanical result adapter; no trajectory axis is inferred.",
            reference_structure_index=None,
            pca_component=None,
        )

    def _mechanical_row(self, position):
        r = self._report
        if r.layout == "mechanical_forces":
            f, a = divmod(position, len(r.first))
            return [int(r.first[a])], r.frames[f]
        return r.first.tolist(), r.frames[0]

    def _mechanical_page(self, offset, size):
        r, rows = self._report, []
        force = r.layout == "mechanical_forces"
        columns = (
            [
                "Structure index",
                "Atom index",
                *(
                    ["Magnitude (kJ/(mol·nm))"]
                    if r.parameters["force_output"] == "magnitude"
                    else ["X (kJ/(mol·nm))", "Y (kJ/(mol·nm))", "Z (kJ/(mol·nm))"]
                ),
            ]
            if force
            else ["Structure index", "Native term", f"Value ({r.unit})"]
        )
        for position in range(offset, min(r.total, offset + size)):
            if force:
                f, a = divmod(position, len(r.first))
                row = [
                    r.frames[f],
                    int(r.first[a]),
                    *[
                        format(float(v), ".9g")
                        for v in np.asarray(r.values[f, a]).reshape(-1)
                    ],
                ]
            else:
                row = [
                    r.frames[0],
                    r.auxiliary["terms"][position],
                    int(r.values[position])
                    if r.parameters["task"] == "mechanical_dof"
                    else format(float(r.values[position]), ".9g"),
                ]
            rows.append(row)
        return dict(
            offset=offset, total=r.total, page_size=size, columns=columns, rows=rows
        )
