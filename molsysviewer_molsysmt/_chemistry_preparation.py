"""Explicit native preparation and reviewed adoption of independent results."""

from dataclasses import dataclass
from inspect import signature
from math import isfinite
from secrets import token_urlsafe
from weakref import ref

from ._construction import CONSTRUCTION_TASKS, FRESH_TASKS, construct

PREPARATION_DEFAULTS = {
    "hydrogen_mode": "pH",
    "engine": "MolSysMT",
    "pH": "7.4",
    "attribute_policy": "strict",
    "title": "",
    "inference_method": "supported_group_templates",
    "bond_cutoff": "2 angstroms",
    "n_cap": "none",
    "c_cap": "none",
    "keep_ids": "no",
    "charge_method": "gasteiger_marsili",
    "forcefield": "",
    "water_model": "",
    "expected_charge": "",
}
REPAIR_TASKS = {
    "infer_bonds",
    "add_bonds",
    "terminal_cappings",
    "remove_hydrogens",
    "autodock_types",
    "partial_charges",
}
PREPARATION_TASKS = {"heavy", "add_hydrogens"} | REPAIR_TASKS | CONSTRUCTION_TASKS


def validate_preparation_parameters(parameters):
    for key, limit in {
        "pH": 64,
        "title": 200,
        "bond_cutoff": 128,
        "forcefield": 200,
        "water_model": 200,
        "expected_charge": 64,
    }.items():
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

    for key, choices in {
        "inference_method": {
            "supported_group_templates",
            "supported_group_templates_with_hydrogen_aliases",
        },
        "n_cap": {"none", "ACE"},
        "c_cap": {"none", "NME", "NHE", "NH2"},
        "keep_ids": {"yes", "no"},
        "charge_method": {"gasteiger_marsili", "forcefield"},
    }.items():
        if not isinstance(parameters[key], str) or parameters[key] not in choices:
            raise ValueError("Choose a supported explicit repair or assignment method.")


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

        if self._parameters["task"] in CONSTRUCTION_TASKS:
            self._prepare_construction()
            return

        def calculate(target):
            status = self._owner.get_sync_status()
            if status["state"] != "synchronized":
                raise ValueError("Update the scene before preparing a separate system.")
            parameters = self._parameters
            total = int(target.structures.n_structures)
            if not total and parameters["task"] not in {
                "infer_bonds",
                "autodock_types",
                "partial_charges",
                "remove_hydrogens",
            }:
                raise ValueError("This preparation requires molecular coordinates.")
            frame = (
                int(self._view.player.index)
                if self._draft["context"] == "current"
                else self._draft["structure_index"]
            )
            if parameters["task"] in {
                "autodock_types",
                "partial_charges",
                "remove_hydrogens",
            }:
                frame = int(self._view.player.index) if total else 0
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
            elif parameters["task"] == "add_hydrogens":
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
            else:
                candidate, operation, scientific, title = self._prepare_repair(
                    target, frame, total
                )
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

    def _prepare_construction(self):
        import molsysmt as msm

        def calculate(target):
            status = self._owner.get_sync_status()
            if status["state"] != "synchronized":
                raise ValueError("Update or recover the scene before construction.")
            candidate, operation, science, title, frames = construct(self, target)
            before = (
                set(msm.get_attributes(target, include_none=False))
                if target is not None
                else set()
            )
            missing = sorted(
                before - set(msm.get_attributes(candidate, include_none=False))
            )
            metadata = self._store_result(
                candidate,
                title=self._parameters["title"].strip() or title,
                operation=operation,
                structure_indices=frames,
                revision=status["target_revision"],
            )
            metadata.update(
                source_atoms=int(target.get_n_atoms()) if target is not None else 0,
                parameters=science,
                missing_attributes=missing[:200],
                attributes_truncated=len(missing) > 200,
                software={"molsysmt": str(msm.__version__)[:200]},
            )
            self._result = metadata
            self._prepared_source = _PreparedSource(
                ref(target) if target is not None else lambda: None,
                status["target_revision"],
            )

        if self._parameters["task"] in FRESH_TASKS:
            # Fresh explicit inputs do not implicitly bind or inspect a primary.
            self._owner._view()
            calculate(self._view.molsys)
        else:
            self._owner._read(calculate, {})

    def _prepare_repair(self, target, frame, total):
        """Keep scientific decisions in public native wrappers and outputs separate."""
        p, task = self._parameters, self._parameters["task"]
        if frame < 0 or (total and frame >= total):
            raise ValueError("The selection structure index is outside this system.")
        state = int(p["state_index"]) if p["state_mode"] == "index" else p["state_mode"]
        methods = {
            "infer_bonds": ("infer_covalent_bonds", "Infer covalent bonds"),
            "add_bonds": ("add_missing_bonds", "Add missing bonds"),
            "terminal_cappings": (
                "add_missing_terminal_cappings",
                "Complete terminal atoms and caps",
            ),
            "remove_hydrogens": (
                "reconcile_protonation",
                "Remove reference-rule hydrogens",
            ),
            "autodock_types": (
                "assign_autodock_atom_types",
                "Assign AutoDock atom types",
            ),
            "partial_charges": ("assign_partial_charges", "Assign partial charges"),
        }
        name, title = methods[task]
        arguments, science = (
            {},
            {
                "task": task,
                "scope": "whole_system",
                "all_source_structures_retained": True,
            },
        )
        if task in {"infer_bonds", "add_bonds", "terminal_cappings"}:
            atoms = self._selection(target, frame)
            if not atoms.size:
                raise ValueError("Choose a nonempty population for this repair.")
            arguments["selection"] = atoms.tolist()
            science.update(
                scope="selected_atoms",
                selected_atoms=int(atoms.size),
                selection_structure=frame,
            )
        if task == "infer_bonds":
            arguments.update(
                structure_indices=[frame] if total else "all",
                chemical_state=state,
                method=p["inference_method"],
                return_report=True,
            )
        elif task == "add_bonds":
            arguments.update(
                max_bond_length=p["bond_cutoff"],
                structure_index=frame,
                engine="MolSysMT",
                in_place=False,
            )
        elif task == "terminal_cappings":
            from molsysmt import basic

            groups = sorted(
                {
                    int(i)
                    for i in basic.get(
                        target,
                        element="atom",
                        selection=atoms.tolist(),
                        group_index=True,
                    )
                }
            )
            # The native composition evaluates the same expression at group and
            # atom levels. A named hierarchy expression is unambiguous at both;
            # a flat integer list would change meaning between those levels.
            arguments["selection"] = "group_index in " + str(groups)
            science.update(
                scope="selected_groups_and_native_components",
                selected_groups=len(groups),
            )
            arguments.update(
                N_terminal=None if p["n_cap"] == "none" else p["n_cap"],
                C_terminal=None if p["c_cap"] == "none" else p["c_cap"],
                pH=self._finite_ph(),
                keep_ids=p["keep_ids"] == "yes",
                engine="MolSysMT",
            )
        elif task == "remove_hydrogens":
            arguments.update(pH=self._finite_ph(), engine="MolSysMT", in_place=False)
        else:
            arguments.update(
                structure_indices=[frame] if total else "all",
                chemical_state=state,
                return_report=True,
            )
            if task == "autodock_types":
                arguments.update(
                    typing_scheme="autodock4", method="chemical_environment"
                )
            else:
                method = p["charge_method"]
                charge = p["expected_charge"].strip()
                try:
                    expected = int(charge) if charge else None
                except ValueError as exc:
                    raise ValueError(
                        "Declare the expected whole-system charge as an integer in elementary charge, or leave it empty."
                    ) from exc
                ff = p["forcefield"].strip() if method == "forcefield" else None
                if method == "forcefield" and not ff:
                    raise ValueError("Name the force field for this charge model.")
                arguments.update(
                    method=method,
                    forcefield=ff,
                    water_model=(p["water_model"].strip() or None)
                    if method == "forcefield"
                    else None,
                    expected_total_charge=expected,
                )
        output = getattr(self._owner.build, name)(**arguments)
        if arguments.get("return_report"):
            candidate = output["molecular_system"]
            science["report_schema"] = str(output["report"]["schema"])[:200]
        else:
            candidate = output
        science.update(
            {
                key: value
                for key, value in arguments.items()
                if key not in {"selection", "return_report"}
            }
        )
        # Native reports/history and bound assignments remain owned by the result;
        # the widget receives bounded scalar provenance, never entire atom arrays.
        return candidate, "molsysmt.build." + name, science, title

    def _finite_ph(self):
        try:
            value = float(self._parameters["pH"])
        except ValueError as exc:
            raise ValueError("Enter a finite numerical pH.") from exc
        if not isfinite(value):
            raise ValueError("Enter a finite numerical pH.")
        return value

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
