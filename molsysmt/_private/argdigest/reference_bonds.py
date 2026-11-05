"""Scoped name/index contracts for the seven reference-bond entry points."""

import numpy as np
from argdigest.core.caller import caller_is_one_of

from molsysmt._private.smonitor import ArgumentError, ArgumentLengthError

from .argument._correspondence_axes import _has_units
from .argument.atom_names import _flat_atom_name_list
from .argument.skip_digestion import digest_skip_digestion
from .argument.sorted import digest_sorted
from .name_resolution import _scheme

DIGEST_OPTIONS = {
    "digestion_source": "molsysmt._private.argdigest.reference_bonds",
    "digestion_style": "registry",
    "strictness": "error",
}

_SCALAR_CALLERS = (
    "molsysmt.element.group.amino_acid.get_bonded_atom_pairs.get_bonded_atom_pairs",
    "molsysmt.element.group.ion.get_bonded_atom_pairs.get_bonded_atom_pairs",
)
_DISPATCHER = "molsysmt.element.group.get_bonded_atom_pairs.get_bonded_atom_pairs"


def _scalar_allowed(caller, group_name, naming_scheme=None):
    if caller_is_one_of(caller, _SCALAR_CALLERS):
        return True
    if caller_is_one_of(caller, (_DISPATCHER,)):
        from molsysmt.element.group.get_group_type import get_group_type_from_group_name

        return get_group_type_from_group_name(
            group_name, naming_scheme=naming_scheme
        ) in {"amino acid", "ion"}
    return False


def _group_name(group_name, caller=None):
    if isinstance(group_name, str):
        return group_name
    raise ArgumentError("group_name", value=group_name, caller=caller)


def _atom_names(atom_names, group_name=None, naming_scheme=None, caller=None):
    if isinstance(atom_names, str) and _scalar_allowed(
        caller, group_name, naming_scheme
    ):
        return [atom_names]
    return _flat_atom_name_list(atom_names, caller=caller)


def _atom_indices(
    atom_indices, atom_names, group_name=None, naming_scheme=None, caller=None
):
    if atom_indices is None:
        return None
    if _has_units(atom_indices) or np.ma.isMaskedArray(atom_indices):
        raise ArgumentError(
            "atom_indices",
            value=atom_indices,
            caller=caller,
            message="Supply unit-free indices without a mask.",
        )
    scalar = isinstance(atom_indices, (int, np.integer)) and not isinstance(
        atom_indices, (bool, np.bool_)
    )
    if (
        scalar
        and len(atom_names) == 1
        and _scalar_allowed(caller, group_name, naming_scheme)
    ):
        values = [atom_indices]
    elif isinstance(atom_indices, (list, tuple, np.ndarray, range)):
        values = np.asarray(atom_indices, dtype=object)
        if values.ndim != 1:
            raise ArgumentError(
                "atom_indices",
                value=atom_indices,
                caller=caller,
                message="Supply a flat integer map with one index per atom name.",
            )
    else:
        raise ArgumentError(
            "atom_indices",
            value=atom_indices,
            caller=caller,
            message="Supply a flat integer map with one index per atom name.",
        )
    upper = np.iinfo(np.int64).max
    if any(
        isinstance(value, (bool, np.bool_))
        or not isinstance(value, (int, np.integer))
        or value < 0
        or value > upper
        for value in values
    ):
        raise ArgumentError(
            "atom_indices",
            value=atom_indices,
            caller=caller,
            message="Atom-index maps require nonnegative int64-range integers, excluding booleans.",
        )
    if len(values) != len(atom_names):
        raise ArgumentLengthError(
            "atom_indices",
            expected=len(atom_names),
            actual=len(values),
            caller=caller,
        )
    # Preserve the two existing digested families' integer-array normalization.
    # Other helpers retain caller scalar types; none mutates the map.
    if caller_is_one_of(caller, _SCALAR_CALLERS):
        return np.array(values, dtype=np.int64)
    return atom_indices if not scalar else values


ARGUMENT_DIGESTERS = {
    "group_name": _group_name,
    "naming_scheme": _scheme,
    "atom_names": _atom_names,
    "atom_indices": _atom_indices,
    "sorted": digest_sorted,
    "skip_digestion": digest_skip_digestion,
}
