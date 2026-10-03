"""Classifying and validating candidate molecular systems."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MolecularSystemKind(str, Enum):
    """Describing whether input items represent one or several systems."""

    SINGLE = "single"
    MULTIPLE = "multiple"
    UNSUPPORTED = "unsupported"


class ValidationStatus(str, Enum):
    """Describing the consistency evidence for a candidate single system."""

    VALID = "valid"
    INVALID = "invalid"
    UNVERIFIED = "unverified"


@dataclass(frozen=True)
class MolecularSystemAssessment:
    """Holding classification and validation evidence."""

    kind: MolecularSystemKind
    validation: ValidationStatus
    forms: tuple[str, ...] = ()
    atom_counts: tuple[int, ...] = ()
    reason: str | None = None

    @property
    def is_valid_single_system(self) -> bool:
        """Returning whether the evidence proves one consistent system."""

        return (
            self.kind is MolecularSystemKind.SINGLE
            and self.validation is ValidationStatus.VALID
        )


def _provides_topology(form_module) -> bool:
    """Return whether a form carries a molecular topology."""

    if getattr(form_module, "piped_topological_attribute", None) is not None:
        return True
    return "molsysmt.Topology" in getattr(form_module, "_convert_to", {})


def _provides_primary_topology(form_module) -> bool:
    """Return whether topology is a primary payload of a form."""

    declared = getattr(form_module, "provides_primary_topology", None)
    if declared is not None:
        return bool(declared)
    if getattr(form_module, "piped_topological_attribute", None) is not None:
        return True
    return bool(
        getattr(form_module, "bonds_are_explicit", False)
        or getattr(form_module, "bonds_can_be_computed", False)
    )


def _provides_structures(form_module) -> bool:
    """Return whether a form carries atom-indexed structural data."""

    if getattr(form_module, "piped_structural_attribute", None) is not None:
        return True
    return "molsysmt.Structures" in getattr(form_module, "_convert_to", {})


def assess_molecular_system(molecular_system) -> MolecularSystemAssessment:
    """Classify an input and validate complementary items when possible."""

    from molsysmt.basic import get, get_form
    from molsysmt.form import _dict_modules

    items = (
        molecular_system
        if isinstance(molecular_system, (list, tuple))
        else [molecular_system]
    )
    if len(items) == 0:
        return MolecularSystemAssessment(
            MolecularSystemKind.UNSUPPORTED,
            ValidationStatus.INVALID,
            reason="The input container is empty.",
        )

    try:
        forms = tuple(get_form(item) for item in items)
    except Exception as error:
        return MolecularSystemAssessment(
            MolecularSystemKind.UNSUPPORTED,
            ValidationStatus.INVALID,
            reason=f"{type(error).__name__}: {error}",
        )

    if len(items) == 1:
        return MolecularSystemAssessment(
            MolecularSystemKind.SINGLE,
            ValidationStatus.VALID,
            forms=forms,
        )

    from molsysmt._private.h5msm import modular_h5msm_axes
    from molsysmt.native import MolSys

    topology_items = 0
    instance_counts = []
    try:
        for item, form in zip(items, forms):
            axes = modular_h5msm_axes(item) if form == "file:h5msm" else None
            if axes is not None:
                topology_items += ("topology", None, "atom") in axes
                instance_counts.append(
                    [size for (_, _, axis), size in axes.items() if axis == "atom"]
                )
            elif isinstance(item, MolSys):
                topology_items += item.topology is not None
                count = item._get_n_atoms()
                instance_counts.append([] if count is None else [count])
            else:
                topology_items += _provides_primary_topology(_dict_modules[form])
                instance_counts.append(None)
    except Exception as error:
        return MolecularSystemAssessment(
            MolecularSystemKind.SINGLE,
            ValidationStatus.UNVERIFIED,
            forms=forms,
            reason=f"Could not inspect domain axes: {type(error).__name__}: {error}",
        )
    if topology_items > 1:
        return MolecularSystemAssessment(
            MolecularSystemKind.MULTIPLE,
            ValidationStatus.VALID,
            forms=forms,
            reason=f"{topology_items} items provide a topology.",
        )

    atom_counts = []
    for item, form, counts in zip(items, forms, instance_counts):
        if counts is not None:
            atom_counts.extend(int(count) for count in counts)
            continue
        form_module = _dict_modules[form]
        if not (
            _provides_topology(form_module)
            or _provides_structures(form_module)
            or getattr(form_module, "provides_atom_domain", False)
        ):
            continue
        try:
            n_atoms = get(
                item,
                element="system",
                n_atoms=True,
                skip_digestion=True,
            )
        except Exception as error:
            return MolecularSystemAssessment(
                MolecularSystemKind.SINGLE,
                ValidationStatus.UNVERIFIED,
                forms=forms,
                atom_counts=tuple(atom_counts),
                reason=(
                    f"Could not obtain 'n_atoms' from form {form!r}: "
                    f"{type(error).__name__}: {error}"
                ),
            )

        if n_atoms is None:
            return MolecularSystemAssessment(
                MolecularSystemKind.SINGLE,
                ValidationStatus.UNVERIFIED,
                forms=forms,
                atom_counts=tuple(atom_counts),
                reason=f"Form {form!r} returned no 'n_atoms' value.",
            )
        atom_counts.append(int(n_atoms))

    if len(set(atom_counts)) > 1:
        return MolecularSystemAssessment(
            MolecularSystemKind.SINGLE,
            ValidationStatus.INVALID,
            forms=forms,
            atom_counts=tuple(atom_counts),
            reason=f"Complementary items have different atom counts: {atom_counts}.",
        )

    return MolecularSystemAssessment(
        MolecularSystemKind.SINGLE,
        ValidationStatus.VALID,
        forms=forms,
        atom_counts=tuple(atom_counts),
    )


def validate_molecular_system_argument(value, argument, caller=None):
    """Return a valid system or raise a classification-specific exception."""

    from molsysmt._private.smonitor import (
        ArgumentError,
        MolecularSystemVerificationError,
        MultipleMolecularSystemsError,
        StructuralInconsistencyError,
    )

    assessment = assess_molecular_system(value)
    if assessment.is_valid_single_system:
        return value
    if assessment.kind is MolecularSystemKind.MULTIPLE:
        raise MultipleMolecularSystemsError(
            n_systems=len(value),
            forms=list(assessment.forms),
            caller=caller,
        )
    if assessment.kind is MolecularSystemKind.SINGLE:
        if assessment.validation is ValidationStatus.INVALID:
            raise StructuralInconsistencyError(reason=assessment.reason, caller=caller)
        if assessment.validation is ValidationStatus.UNVERIFIED:
            raise MolecularSystemVerificationError(
                forms=list(assessment.forms),
                reason=assessment.reason,
                caller=caller,
            )
    raise ArgumentError(argument, value=value, caller=caller, message=None)
