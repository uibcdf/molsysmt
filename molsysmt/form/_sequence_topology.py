"""Interpret declared sequence codes; atom construction belongs to explicit tools."""

from molsysmt._private.smonitor import ArgumentError, NotWithThisFormError
from molsysmt._private.variables import is_all
from molsysmt.element.group.amino_acid.codes import aa1_to_aa3


def group_names(text, width, *, caller):
    if len(text) % width:
        raise ArgumentError(
            "item",
            caller=caller,
            message="Sequence text must contain complete group codes.",
        )
    codes = [text[i : i + width].upper() for i in range(0, len(text), width)]
    if width == 1:
        if any(code not in aa1_to_aa3 for code in codes):
            raise ArgumentError(
                "item",
                caller=caller,
                message="Topology conversion requires native amino-acid codes; gaps, stops and unsupported symbols need explicit interpretation.",
            )
        return [aa1_to_aa3[code] for code in codes]
    if any(not code.isascii() or not code.isalpha() for code in codes):
        raise ArgumentError(
            "item",
            caller=caller,
            message="Three-letter sequence groups must be complete alphabetic codes.",
        )
    return codes


def from_string(item, width, group_indices, structure_indices, *, caller):
    from molsysmt.native._sequence_topology import from_group_records

    from ._sequence_selection import extract

    # Validate the whole source before selection: an empty output cannot hide a
    # malformed suffix or silently remove a stop/gap from the declared sequence.
    group_names(item.removeprefix(f"amino_acids_{width}:"), width, caller=caller)
    selected = extract(
        item, width, "all", group_indices, structure_indices, caller=caller
    )
    names = group_names(
        selected.removeprefix(f"amino_acids_{width}:"), width, caller=caller
    )
    return from_group_records([{"groups": names}])


def require_no_structures(structure_indices, *, caller, form):
    if not is_all(structure_indices):
        raise NotWithThisFormError(
            caller=caller,
            form=form,
            requested_attribute="structure_indices",
            message="Sequence forms do not contain structures.",
        )
