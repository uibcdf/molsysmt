"""Sparse native interaction inspection and deliberate scientific/scene adoption."""

import json
from collections.abc import Mapping
from itertools import islice
from secrets import token_urlsafe
from weakref import ref

import numpy as np

from ._task_panel import _structures

INTERACTION_METHODS = {
    "interaction_hbonds": ("hbonds", "get_hbonds"),
    "interaction_disulfides": ("disulfides", "get_disulfide_candidates"),
    "interaction_ionic": ("ionic", "get_ionic_interactions"),
    "interaction_hydrophobic": ("hydrophobic", "get_hydrophobic_interactions"),
    "interaction_halogen": ("halogen_bonds", "get_halogen_bonds"),
    "interaction_metal": ("metal_coordination", "get_metal_coordination"),
    "interaction_pi_pi": ("pi_pi", "get_pi_pi_interactions"),
    "interaction_cation_pi": ("cation_pi", "get_cation_pi_interactions"),
    "interaction_water": ("water_bridges", "get_water_bridges"),
}
INTERACTION_DEFAULTS = dict(
    interaction_mode="internal",
    hbond_method="baker_hubbard",
    interaction_distance="",
    interaction_angle="",
    interaction_offset="",
    interaction_planarity="",
    interaction_profile="",
    interaction_donor_angles="",
    interaction_acceptor_angles="",
    water_order="1",
)


def validate_interaction_parameters(p):
    for key, choices in {
        "interaction_mode": {"internal", "incident", "between"},
        "hbond_method": {
            "baker_hubbard",
            "wernet_nilsson",
            "donor_acceptor_distance_angle",
        },
        "water_order": {"1", "2"},
    }.items():
        if not isinstance(p[key], str) or p[key] not in choices:
            raise ValueError(
                "Choose supported interaction scope, method and water order."
            )
    for key in set(INTERACTION_DEFAULTS) - {
        "interaction_mode",
        "hbond_method",
        "water_order",
    }:
        if not isinstance(p[key], str) or len(p[key]) > 200:
            raise ValueError(
                "Enter bounded interaction settings with explicit physical units."
            )


def _preview(value, *, limit=4096):
    """Bound display text only; full native metadata remain on the result."""

    def bounded(v, depth=0):
        if depth > 6:
            return "… (nested preview)"
        if isinstance(v, np.ndarray):
            return bounded(list(islice(v, 20)) if v.ndim else v.item(), depth + 1)
        if isinstance(v, np.generic):
            return v.item()
        if isinstance(v, Mapping):
            out = {
                str(k)[:100]: bounded(item, depth + 1)
                for k, item in islice(v.items(), 20)
            }
            if len(v) > 20:
                out["…"] = f"{len(v)} entries (preview)"
            return out
        if isinstance(v, (tuple, list)):
            out = [bounded(item, depth + 1) for item in v[:20]]
            return out + [f"… ({len(v)} entries)"] if len(v) > 20 else out
        if isinstance(v, str):
            return v[:500] + ("…" if len(v) > 500 else "")
        if isinstance(v, (bool, int, float, type(None))):
            return v
        return str(v)[:500]

    text = json.dumps(bounded(value), ensure_ascii=True)
    return (
        text
        if len(text) <= limit
        else text[:limit] + "… (preview; full value in Python)"
    )


class _InteractionReports:
    def _calculate_interactions(self, target, status, atoms):
        import molsysmt as msm

        p = self._parameters
        family, name = INTERACTION_METHODS[p["task"]]
        disulfide = family == "disulfides"
        if disulfide and p["interaction_mode"] != "internal":
            raise ValueError(
                "The disulfide-candidate reader supports one internal atom population; no additional scope is inferred."
            )
        second = (
            self._population(target, self._second, status)
            if p["interaction_mode"] == "between"
            else np.empty(0, dtype=np.int64)
        )
        requested = _structures(
            p["structures"],
            p["indices"],
            int(target.structures.n_structures),
            int(self._view.player.index),
            allow_repeated=True,
        )
        args = dict(
            selection=atoms.tolist(),
            structure_indices=requested,
            pbc=p["pbc"],
            output_type="molsysmt.Interactions",
        )
        if disulfide:
            if p["interaction_distance"].strip():
                args["max_bond_length"] = p["interaction_distance"].strip()
        else:
            state = p["graph_state"]
            if state == "index":
                try:
                    state = int(p["graph_state_index"])
                except ValueError as error:
                    raise ValueError("Enter a chemical-state index.") from error
                if state < 0:
                    raise ValueError("Enter a nonnegative chemical-state index.")
            args.update(
                chemical_state=state,
                selection_mode=p["interaction_mode"],
                assume_complete_connectivity=p["assume_complete"],
                heavy_mode="auto",
            )
            if second.size:
                args["selection_2"] = second.tolist()
            if p["interaction_distance"].strip():
                args["distance_threshold"] = p["interaction_distance"].strip()
            elif family == "ionic":
                raise ValueError(
                    "Ionic contacts require an explicit distance threshold with length units; no universal cutoff is supplied."
                )
            if family != "ionic" and p["interaction_profile"].strip():
                args["profile"] = p["interaction_profile"].strip()
            if family in {"hbonds", "water_bridges"}:
                args["method" if family == "hbonds" else "hbond_method"] = p[
                    "hbond_method"
                ]
            if (
                family in {"hbonds", "water_bridges", "pi_pi", "cation_pi"}
                and p["interaction_angle"].strip()
            ):
                args["angle_threshold"] = p["interaction_angle"].strip()
            if family in {"pi_pi", "cation_pi"}:
                for gui, native in [
                    ("interaction_offset", "offset_threshold"),
                    ("interaction_planarity", "planarity_threshold"),
                ]:
                    if p[gui].strip():
                        args[native] = p[gui].strip()
                args["max_cyclic_block_size"] = 256
            if family == "halogen_bonds":
                for gui, native in [
                    ("interaction_donor_angles", "donor_angle_range"),
                    ("interaction_acceptor_angles", "acceptor_angle_range"),
                ]:
                    if p[gui].strip():
                        try:
                            angles = json.loads(p[gui])
                        except json.JSONDecodeError as error:
                            raise ValueError(
                                "Enter a JSON pair of angles with physical units."
                            ) from error
                        if (
                            not isinstance(angles, list)
                            or len(angles) != 2
                            or not all(isinstance(v, str) for v in angles)
                        ):
                            raise ValueError(
                                "Angle ranges require two explicit unit-bearing strings."
                            )
                        args[native] = tuple(angles)
            if family == "water_bridges":
                args["order"] = int(p["water_order"])
            if family != "ionic":
                args["max_matches"] = 100000
        reader = getattr(getattr(self._owner.interactions, family), name)
        native = reader(**args)
        if not isinstance(native, msm.Interactions):
            raise ValueError(
                "The native detector did not return its declared sparse interaction result."
            )
        if native.n_atoms != int(target.get_n_atoms()) or native.n_structures != int(
            target.structures.n_structures
        ):
            raise ValueError(
                "Native interaction axes do not match the current source system."
            )
        # Native detection owns structure deduplication and evaluated-empty
        # coverage. Do not turn repeated requests into duplicated observations.
        return self._report_type(
            token=token_urlsafe(18),
            target=ref(target),
            revision=status["target_revision"],
            visible_frame=int(self._view.player.index),
            first_draft=dict(self._draft),
            second_draft=dict(self._second),
            parameters=dict(p),
            frames=requested,
            first=atoms,
            second=second,
            selections=(False, False),
            values=native,
            native_values=native,
            unit=None,
            auxiliary={
                "method": "molsysmt.interactions." + family + "." + name,
                "stored_name": None,
                "stored_target": None,
            },
            offsets=None,
            layout="interaction_occurrences",
            total=int(native.n_interactions),
            periodic=bool(p["pbc"] and target.structures.box is not None),
            software=str(msm.__version__)[:200],
        )

    def _interaction_summary(self):
        r = self._report
        native = r.native_values
        coverage = native.evaluated_structure_indices
        return dict(
            id=r.token,
            method=r.auxiliary["method"],
            software=dict(native.software),
            rows=r.total,
            unit=None,
            first_atoms=len(r.first),
            second_atoms=len(r.second),
            structure_indices=r.frames[:200],
            structures_truncated=len(r.frames) > 200,
            structure_count=len(r.frames),
            source_revision=r.revision,
            family="interactions",
            result_axis="occurrence",
            periodic=r.periodic,
            requested_pbc=r.parameters["pbc"],
            evaluated_structure_indices=coverage[:200].tolist(),
            evaluated_structure_count=len(coverage),
            evaluated_structures_truncated=len(coverage) > 200,
            stored_name=r.auxiliary["stored_name"],
            scientific_method=native.method,
            parameters_preview=_preview(native.parameters),
            measure_units_preview=_preview(native.measure_units),
            evaluation_scope_preview=_preview(
                dict(
                    mode=native.evaluation_mode,
                    declared_atom_indices=native.evaluation_atom_indices,
                    declared_atom_indices_b=native.evaluation_atom_indices_b,
                    declared_universe_indices=native.evaluation_universe_indices,
                    note="Null axes retain native implicit full-scope semantics; inspect evaluation_scope in Python for the expanded declaration.",
                )
            ),
            native_experimental=True,
            disk_backed=False,
            notice="Experimental native sparse analysis. "
            + (
                "Periodic geometry requested with a stored box. "
                if r.periodic
                else "No box is stored: native nonperiodic geometry is used. "
                if r.parameters["pbc"]
                else "Nonperiodic geometry requested. "
            )
            + "An evaluated structure with zero occurrences is not an unevaluated structure. Requested repetitions follow native detector deduplication. No bonds, hydrogens or chemical assignments are inferred by this panel.",
            live_distance_unavailable="An interaction occurrence has explicit roles and may have compound participants; it is not a generic pair distance.",
            plot_unavailable="No interaction occupancy or trajectory aggregation is inferred.",
            reference_structure_index=None,
            pca_component=None,
        )

    def _interaction_native_page(self, offset, limit):
        return self._report.native_values.to_page(
            offset=offset, limit=limit, max_participant_atoms=10000
        )

    @staticmethod
    def _page_relation(page, i):
        relation = int(page["relation_indices"][i])
        compact = int(np.searchsorted(page["relation_catalog_indices"], relation))
        start, end = page["relation_participant_offsets"][compact : compact + 2]
        members = []
        for j in range(start, end):
            a, b = page["participant_atom_offsets"][j : j + 2]
            members.append(
                (
                    str(page["participant_roles"][j]),
                    page["participant_atoms"][a:b].tolist(),
                )
            )
        return str(page["relation_types"][compact]), members

    def _interaction_row(self, position):
        page = self._interaction_native_page(position, 1)
        _, participants = self._page_relation(page, 0)
        return list(dict.fromkeys(a for _, atoms in participants for a in atoms)), int(
            page["structure_indices"][0]
        )

    def _interaction_page(self, offset, size):
        page = self._interaction_native_page(offset, size)
        rows = []
        for i, occurrence in enumerate(page["occurrence_indices"]):
            kind, members = self._page_relation(page, i)
            roles = "; ".join(
                f"{role}: {atoms[:12]}" + ("…" if len(atoms) > 12 else "")
                for role, atoms in members[:4]
            )
            if len(members) > 4:
                roles += f"; … ({len(members)} participants)"
            measures = {
                name: dict(value=values[i], unit=page["measure_units"].get(name))
                for name, values in page["measurements"].items()
            }
            images = None
            if page["image_offsets"] is not None:
                a, b = page["image_offsets"][i : i + 2]
                images = page["image_vectors"][a:b]
            rows.append(
                [
                    int(page["structure_indices"][i]),
                    int(occurrence),
                    kind,
                    roles,
                    _preview(measures, limit=1200),
                    str(page["evidence"][i])[:300],
                    _preview(images, limit=300),
                ]
            )
        return dict(
            offset=offset,
            total=self._report.total,
            page_size=size,
            columns=[
                "Structure index",
                "Occurrence index",
                "Interaction type",
                "Roles and source atoms (preview)",
                "Native measures and units (preview)",
                "Evidence",
                "Periodic images (preview)",
            ],
            rows=rows,
        )

    def _adopt_interactions(self, action, payload, request_id):
        report = self._current_report(self._context())
        if (
            report is None
            or report.parameters["task"] not in INTERACTION_METHODS
            or payload.get("report_id") != report.token
        ):
            raise ValueError(
                "That interaction result has expired; calculate it again for the current source."
            )
        if self._owner.get_sync_status()["state"] != "synchronized":
            raise ValueError(
                "Synchronize the current scene before adopting interaction results."
            )
        name = payload.get("analysis_name")
        if not isinstance(name, str) or not name.strip() or len(name) > 200:
            raise ValueError("Enter a bounded name for the saved analysis.")
        name = name.strip()
        if action == "store_interactions":
            # This result was calculated against this unchanged primary system;
            # the declaration comes from that managed source lifetime, not IDs.
            self._view.interactions.attach(
                report.native_values, name=name, assume_aligned=True
            )
            report.auxiliary.update(
                stored_name=name,
                stored_target=ref(self._view.molsys.interactions[name]),
            )
            message = f"Stored analysis {name}. No visual set was added; H5MSM can preserve the named scientific result."
        else:
            stored = report.auxiliary["stored_target"]
            if (
                name != report.auxiliary["stored_name"]
                or stored is None
                or self._view.molsys.interactions.get(name) is not stored()
            ):
                raise ValueError(
                    "First store this result under that name; a replaced or removed analysis must be reviewed again."
                )
            obj = self._view.interactions.add(name)
            message = f"Added visual set {obj.tag} for {name}. Core Interactions owns visibility and style; Clear keeps the scientific analysis and visual set."
        self._publish(
            stage="scene",
            message=message,
            request_id=request_id,
            scene_action={"id": action, "analysis_name": name},
        )
