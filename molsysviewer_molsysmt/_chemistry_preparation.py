"""Explicit native preparation and reviewed adoption of independent results."""

from dataclasses import dataclass
from inspect import signature
from math import isfinite
from secrets import token_urlsafe
from weakref import ref

PREPARATION_DEFAULTS = {
    "hydrogen_mode": "pH",
    "engine": "MolSysMT",
    "pH": "7.4",
    "attribute_policy": "strict",
    "title": "",
}
PREPARATION_TASKS = {"heavy", "add_hydrogens"}


def validate_preparation_parameters(parameters):
    for key, limit in {"pH": 64, "title": 200}.items():
        if not isinstance(parameters[key], str) or len(parameters[key]) > limit:
            raise ValueError("Enter bounded preparation parameters and a result title.")
    if (
        parameters["hydrogen_mode"] not in {"pH", "fixed_chemical_state"}
        or parameters["engine"] not in {"MolSysMT", "OpenMM", "PDBFixer"}
        or parameters["attribute_policy"] not in {"strict", "intersection"}
    ):
        raise ValueError(
            "Choose a supported preparation mode, engine and attribute policy."
        )


@dataclass(frozen=True)
class _PreparedSource:
    target: object
    revision: int


@dataclass(frozen=True)
class _ReplacementReview:
    token: str
    result_id: str
    candidate: object
    revision: int


class _ChemistryPreparation:
    """Private task orchestration; scientific functions remain the expert API."""

    def _preparation_packet(self, context):
        self._refresh_result()
        if self._result is None:
            self._prepared_source = self._adoption = None
        source = self._prepared_source
        supports_replace = (
            "expected_revision"
            in signature(self._view.addons.manager.system_edits.replace).parameters
        )
        current = bool(
            self._result
            and supports_replace
            and source
            and source.target() is self._view.molsys
            and source.revision == context.get("target_revision")
            and context.get("state") == "synchronized"
        )
        if not current:
            self._adoption = None
        return {
            "result": self._result,
            "can_replace": current,
            "replacement_supported": supports_replace,
            "replacement": {"token": self._adoption.token} if self._adoption else None,
        }

    def _prepare_result(self):
        import molsysmt as msm

        if self._result is not None:
            raise ValueError(
                "Leave or close the current result before preparing another."
            )

        def calculate(target):
            status = self._owner.get_sync_status()
            if status["state"] != "synchronized":
                raise ValueError("Update the scene before preparing a separate system.")
            parameters = self._parameters
            total = int(target.structures.n_structures)
            if not total:
                raise ValueError("Preparation requires molecular coordinates.")
            frame = (
                int(self._view.player.index)
                if self._draft["context"] == "current"
                else self._draft["structure_index"]
            )
            before = set(msm.basic.get_attributes(target, include_none=False))
            if parameters["task"] == "heavy":
                if frame >= total:
                    raise ValueError(
                        "The selection structure index is outside this system."
                    )
                atoms = self._selection(target, frame)
                if not atoms.size:
                    raise ValueError(
                        "Choose a nonempty selection for heavy-atom completion."
                    )
                # This native preparation selects groups. Resolve the shared
                # atom editor through the public stable hierarchy rather than
                # passing atom positions as numeric group positions.
                groups = sorted(
                    set(
                        int(i)
                        for i in msm.basic.get(
                            target,
                            element="atom",
                            selection=atoms.tolist(),
                            group_index=True,
                        )
                    )
                )
                if parameters["engine"] == "OpenMM":
                    raise ValueError(
                        "Choose MolSysMT or PDBFixer for heavy-atom completion."
                    )
                candidate = self._owner.build.add_missing_heavy_atoms(
                    selection=groups,
                    engine=parameters["engine"],
                    attribute_policy=parameters["attribute_policy"],
                )
                operation = "molsysmt.build.add_missing_heavy_atoms"
                scientific = {
                    "selection_atoms": int(atoms.size),
                    "selected_groups": len(groups),
                    "selection_structure": frame,
                    "engine": parameters["engine"],
                    "attribute_policy": parameters["attribute_policy"],
                }
                title = "Heavy-atom completion"
            else:
                # Native fixed-state preparation requires an isolated structure;
                # legacy engines are also only qualified here on one structure.
                # Never silently select the visible structure or extract atoms.
                if total != 1:
                    raise ValueError(
                        "Extract one structure in System before adding hydrogens. "
                        "This operation does not extract a structure automatically."
                    )
                fixed = parameters["hydrogen_mode"] == "fixed_chemical_state"
                state = (
                    int(parameters["state_index"])
                    if parameters["state_mode"] == "index"
                    else parameters["state_mode"]
                )
                try:
                    pH = None if fixed else float(parameters["pH"])
                except ValueError as exc:
                    raise ValueError("Enter a finite numerical pH.") from exc
                if not fixed and not isfinite(pH):
                    raise ValueError("Enter a finite numerical pH.")
                arguments = {
                    "mode": parameters["hydrogen_mode"],
                    "engine": "RDKit" if fixed else parameters["engine"],
                    "pH": pH,
                }
                if fixed:
                    arguments.update(
                        chemical_state=state,
                        structure_indices=[0],
                        return_report=True,
                        attribute_policy=parameters["attribute_policy"],
                    )
                output = self._owner.build.add_missing_hydrogens(**arguments)
                candidate = output["molecular_system"] if fixed else output
                operation = "molsysmt.build.add_missing_hydrogens"
                scientific = dict(
                    arguments, structure_indices=[0], scope="whole_system"
                )
                # Only bounded scalar facts cross the GUI boundary. The full
                # native report/history stays with its independent molecular owner.
                if fixed:
                    scientific.update(
                        report_schema=output["report"]["schema"],
                        added_hydrogens=int(output["report"]["n_added_hydrogens"]),
                    )
                title = "Hydrogen completion"
            missing = sorted(
                before - set(msm.basic.get_attributes(candidate, include_none=False))
            )
            metadata = self._store_result(
                candidate,
                title=parameters["title"].strip() or title,
                operation=operation,
                structure_indices=list(range(total)),
                revision=status["target_revision"],
            )
            metadata.update(
                source_atoms=int(target.get_n_atoms()),
                parameters=scientific,
                missing_attributes=missing[:200],
                attributes_truncated=len(missing) > 200,
                # This comparison is availability, not a proof that all other
                # attributes/values or scientific interpretations are unchanged.
                software={"molsysmt": str(msm.__version__)[:200]},
            )
            self._result = metadata
            self._prepared_source = _PreparedSource(
                ref(target), status["target_revision"]
            )

        self._owner._read(calculate, {})

    def _review_prepared_replacement(self):
        if not self._preparation_packet(self._context())["can_replace"]:
            raise ValueError(
                "The source changed or needs recovery. Keep the separate result; prepare again before replacement."
            )
        candidate_view = self._view.addons.manager.presentations.get(self._result["id"])

        def review(candidate):
            status = candidate_view.addons.manager.system_edits.get_status()
            if status["state"] != "synchronized":
                raise ValueError("Update the result view before reviewing replacement.")
            return _ReplacementReview(
                token_urlsafe(18),
                self._result["id"],
                ref(candidate),
                status["target_revision"],
            )

        self._adoption = candidate_view.addons.manager.system_edits.read(review)

    def _adopt_prepared_result(self, token):
        import molsysmt as msm

        review, self._adoption = self._adoption, None
        if (
            review is None
            or review.token != token
            or self._result is None
            or review.result_id != self._result["id"]
        ):
            raise ValueError(
                "This replacement review has expired. Review the result again."
            )
        source = self._prepared_source
        candidate_view = self._view.addons.manager.presentations.get(review.result_id)

        def copy(candidate):
            status = candidate_view.addons.manager.system_edits.get_status()
            if (
                candidate is not review.candidate()
                or status["target_revision"] != review.revision
                or status["state"] != "synchronized"
            ):
                raise ValueError("The result changed after review. Review it again.")
            # Always isolate the replacement, even if the result was not yet
            # displayed. A later presentation must never share a mutable primary.
            return msm.basic.copy(candidate)

        replacement = candidate_view.addons.manager.system_edits.read(copy)
        self._view.addons.manager.system_edits.replace(
            replacement,
            expected_target=source.target(),
            expected_revision=source.revision,
        )
        self._result["adopted"] = True
        self._prepared_source = None
        self._invalidate_peers()

    def _preparation_action(self, action_id, payload, request_id):
        if action_id == "prepare":
            if self._parameters["task"] not in PREPARATION_TASKS:
                raise ValueError("Choose a molecular preparation task first.")
            self._prepare_result()
            message = (
                "Separate result prepared. The source system and scene are unchanged."
            )
        elif action_id == "replacement.review":
            self._review_prepared_replacement()
            message = "Review replacement before applying it."
        elif action_id == "replacement.apply":
            self._adopt_prepared_result(payload.get("token"))
            message = "The prepared system is now loaded. The separate result remains independent."
        elif action_id == "replacement.back":
            self._adoption = None
            message = "Replacement cancelled. Molecular data are unchanged."
        elif action_id == "result.new":
            self._discard_unpresented_result()
            self._prepared_source = self._adoption = None
            message = (
                "Ready for another preparation. Already presented views remain open."
            )
        elif action_id == "result.discard":
            if self._result is not None:
                self._view.addons.manager.presentations.close(self._result["id"])
            self._result = self._prepared_source = self._adoption = None
            message = "Separate result closed. The source system is unchanged."
        else:
            raise ValueError("Unsupported preparation action.")
        self._publish(stage="prepared", message=message, request_id=request_id)
