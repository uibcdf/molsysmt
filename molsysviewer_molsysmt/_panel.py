"""Selection review and managed removal over the existing expert edit adapter."""

from dataclasses import dataclass
from secrets import token_urlsafe
from weakref import ref

import numpy as np
from smonitor import signal

from ._panel_frontend import CSS, ESM
from ._task_panel import _draft, _MolecularTaskPanel, _structures

_REMOVAL_COMPLETED = "Selected atoms removed. The view is up to date."


@dataclass
class _Review:
    token: str
    target: object
    revision: int
    structures: int
    frame: int
    draft: dict
    indices: np.ndarray
    groups: int | None


@dataclass(frozen=True)
class _Outcome:
    target: object
    revision: int
    draft: dict


class _SystemPanel(_MolecularTaskPanel):
    _esm = ESM
    _css = CSS

    def __init__(self, view=None, **kwargs):
        super().__init__(view=view, **kwargs)
        self._task = "remove"
        self._result_draft = {"structures": "all", "indices": "", "title": ""}

    def _diagnostic_inputs(self):
        return (dict(self._draft), self._task, dict(self._result_draft))

    def _publish(self, *, stage="select", message="", request_id=0):
        if not self._alive or self._view is None or self._view.closed:
            return
        context = self._context()
        self._refresh_result()
        stage, message = self._retained_diagnostic(context, stage, message)
        outcome = self._outcome
        if outcome is not None:
            if (
                context.get("state") != "synchronized"
                or context.get("target_revision") != outcome.revision
                or self._view.molsys is not outcome.target()
                or self._draft != outcome.draft
            ):
                self._outcome = None
            elif stage == "select" and not message:
                # The host refreshes context after synchronization. Keep the
                # completed outcome, without retaining indices or a review token.
                stage, message = "done", _REMOVAL_COMPLETED
        review = self._review
        presentation_service = getattr(self._view.addons.manager, "presentations", None)
        packet = {
            "request_id": request_id,
            "draft": dict(self._draft),
            "context": context,
            "stage": stage,
            "message": message,
            "task": self._task,
            "result_draft": dict(self._result_draft),
            "result": self._result,
            "destinations": list(getattr(presentation_service, "destinations", ())),
        }
        if review is not None:
            packet["review"] = {
                "token": review.token,
                "remove_atoms": int(review.indices.size),
                "keep_atoms": context["n_atoms"] - int(review.indices.size),
                "n_structures": review.structures,
                "selection_structure": review.frame,
                "n_groups": review.groups,
            }
        if self._alive and self._view is not None and not self._view.closed:
            self.push_state(packet)

    def _create_result(self):
        service = getattr(self._view.addons.manager, "presentations", None)
        if (
            service is None
            or not callable(getattr(service, "prepare", None))
            or not service.destinations
        ):
            raise RuntimeError(
                "Update the Viewer host to present independent molecular results."
            )
        self._discard_unpresented_result()

        def calculate(target):
            status = self._owner.get_sync_status()
            if status["state"] != "synchronized":
                raise ValueError(
                    "Update the view before creating an independent result."
                )
            total = int(target.structures.n_structures)
            frame = (
                int(self._view.player.index)
                if self._draft["context"] == "current"
                else self._draft["structure_index"]
            )
            if frame >= total:
                raise ValueError(
                    "The selection structure index is outside this system."
                )
            if self._task == "copy":
                candidate = self._owner.basic.copy()
                structure_indices = list(range(total))
                operation = "molsysmt.basic.copy"
            else:
                atoms = self._selection(target, frame, unique=False)
                if not atoms.size:
                    raise ValueError(
                        "No atoms match this selection. Choose a nonempty subset."
                    )
                structure_indices = _structures(
                    self._result_draft["structures"],
                    self._result_draft["indices"],
                    total,
                    int(self._view.player.index),
                )
                candidate = self._owner.basic.extract(
                    selection=atoms.tolist(), structure_indices=structure_indices
                )
                operation = "molsysmt.basic.extract"
            title = self._result_draft["title"].strip() or (
                "System copy" if self._task == "copy" else "Extracted subset"
            )
            return self._store_result(
                candidate,
                title=title,
                operation=operation,
                structure_indices=structure_indices,
                revision=status["target_revision"],
            )

        self._result = self._owner._read(calculate, {})

    def _result_action(self, action_id, payload, request_id):
        self._refresh_result()
        if set(payload) - {"request_id", "draft", "result_draft", "task"}:
            raise ValueError("The result request contains unsupported fields.")
        if "draft" in payload:
            self._draft = _draft(payload["draft"])
        if "result_draft" in payload:
            draft = payload["result_draft"]
            if not isinstance(draft, dict) or set(draft) != {
                "structures",
                "indices",
                "title",
            }:
                raise ValueError("Choose a valid result scope and title.")
            if (
                draft["structures"] not in {"all", "current", "indices"}
                or not isinstance(draft["indices"], str)
                or len(draft["indices"]) > 4096
                or not isinstance(draft["title"], str)
                or len(draft["title"]) > 200
            ):
                raise ValueError(
                    "Choose a valid result scope and a title of at most 200 characters."
                )
            self._result_draft = dict(draft)
        if action_id == "result.task":
            task = payload.get("task")
            if task not in {"remove", "extract", "copy"}:
                raise ValueError("Choose a supported System task.")
            self._discard_unpresented_result()
            self._review = None
            self._task = task
        elif action_id == "result.create":
            if self._task not in {"extract", "copy"}:
                raise ValueError("Choose Extract subset or Copy system first.")
            if self._result is not None:
                raise ValueError(
                    "Close or leave the previous result before calculating another."
                )
            self._create_result()
        elif action_id == "result.new":
            self._discard_unpresented_result()
        elif action_id == "result.discard":
            if self._result is not None:
                service = self._view.addons.manager.presentations
                if any(item["id"] == self._result["id"] for item in service.records()):
                    service.close(self._result["id"])
                self._result = None
        else:
            raise ValueError("This result action is unavailable.")
        self._publish(
            stage="result" if self._result else "select", request_id=request_id
        )

    def _prepare_review(self, target):
        import pandas as pd

        from molsysmt import basic

        status = self._owner.get_sync_status()
        if status["state"] != "synchronized":
            raise ValueError("Update the view before reviewing a scene selection.")
        count = int(target.get_n_atoms())
        structures = int(target.structures.n_structures)
        frame = (
            int(self._view.player.index)
            if self._draft["context"] == "current"
            else self._draft["structure_index"]
        )
        if frame >= structures:
            raise ValueError("The selection structure index is outside this system.")
        indices = self._selection(target, frame)
        if indices.ndim != 1 or np.any(indices < 0) or np.any(indices >= count):
            raise ValueError("The selection contains atom indices outside this system.")
        if indices.size == count:
            raise ValueError(
                "This selects every atom. Choose a subset; clearing the view is a separate action."
            )
        if not indices.size:
            return None
        groups = basic.get(
            target, selection=indices.tolist(), element="atom", group_index=True
        )
        values = np.asarray(groups, dtype=object).reshape(-1)
        known = [int(i) for i in values if not pd.isna(i) and int(i) >= 0]
        n_groups = len(set(known)) if len(known) == indices.size else None
        indices = indices.copy()
        indices.setflags(write=False)
        return _Review(
            token_urlsafe(24),
            ref(target),
            status["target_revision"],
            structures,
            frame,
            dict(self._draft),
            indices,
            n_groups,
        )

    def _remove(self, token):
        review, self._review = self._review, None
        if review is None or token != review.token:
            raise ValueError("This review has expired. Review the selection again.")
        coordinator = self._view.addons.manager.system_edits

        def prepare(target):
            status = self._owner.get_sync_status()
            frame = (
                int(self._view.player.index)
                if self._draft["context"] == "current"
                else self._draft["structure_index"]
            )
            if (
                target is not review.target()
                or status["target_revision"] != review.revision
                or status["pending_operations"]
                or int(target.structures.n_structures) != review.structures
                or self._draft != review.draft
                or frame != review.frame
            ):
                raise ValueError(
                    "The system or selection context changed. Review the selection again."
                )
            if self._draft["source"] in {
                "current",
                "saved",
                "region",
            } and not np.array_equal(self._selection(target, frame), review.indices):
                raise ValueError(
                    "The selected atoms changed. Review the selection again."
                )
            # Reuse precisely the preparation adapter used by expert remove.
            # The precondition and native publication share one host lock.
            return self._owner.basic._prepare_removal(
                target,
                {
                    "selection": review.indices.tolist(),
                    "structure_indices": None,
                    "to_form": None,
                    "syntax": "MolSysMT",
                    "in_place": True,
                    "skip_digestion": False,
                },
            )

        coordinator.execute(prepare, name="molsysmt.basic.remove", update_view=True)
        self._invalidate_peers()
        return review

    @signal(tags=["addon", "panel"], exception_level="DEBUG")
    def _perform_action(self, action_id, payload, request_id):
        if isinstance(action_id, str) and action_id.startswith("result."):
            self._result_action(action_id, payload, request_id)
            return
        if set(payload) - {"request_id", "draft", "token"}:
            raise ValueError("The panel request contains unsupported fields.")
        if "draft" in payload:
            draft = _draft(payload["draft"])
            if draft != self._draft:
                self._review = None
                self._outcome = None
            self._draft = draft
            self.set_state({"system_draft": dict(draft)})
        if action_id == "refresh":
            self._review = None
            self._publish(request_id=request_id)
            return
        if self._task != "remove":
            raise ValueError(
                "Choose Remove atoms before requesting a molecular removal."
            )
        self._outcome = None
        if action_id not in {"review", "remove", "back"}:
            raise ValueError("This molecular task is not available.")
        if action_id == "back":
            self._review = None
            self._publish(request_id=request_id)
        elif action_id == "review":
            self._review = None
            self._review = self._owner._read(
                lambda target: self._prepare_review(target), {}
            )
            self._publish(
                stage="review" if self._review is not None else "no_matches",
                message=""
                if self._review is not None
                else "Nothing to remove: no atoms match this selection.",
                request_id=request_id,
            )
        else:
            review = self._remove(payload.get("token"))
            # Nonempty removal is one managed edit. A competing edit/replacement
            # cannot be mistaken for this outcome: publication checks its target
            # and expected revision, rather than tagging a later observed status.
            self._outcome = _Outcome(
                review.target, review.revision + 1, dict(review.draft)
            )
            self._publish(
                stage="done",
                message=_REMOVAL_COMPLETED,
                request_id=request_id,
            )
