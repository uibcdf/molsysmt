"""Validate scalar atom-reference queries independently of molecular forms."""

import math
from numbers import Real

import numpy as np

from molsysmt._private.smonitor import ArgumentError

from .argument.atom_names import _flat_atom_name_list
from .name_resolution import ARGUMENT_DIGESTERS as NAMING_DIGESTERS

DIGEST_OPTIONS = {
    "digestion_source": "molsysmt._private.argdigest.atom_expectations",
    "digestion_style": "registry",
    "strictness": "error",
}


def _present_atom_names(present_atom_names, caller=None):
    if present_atom_names is None:
        return None
    if np.ma.isMaskedArray(present_atom_names):
        raise ArgumentError(
            "present_atom_names", value=present_atom_names, caller=caller
        )
    return _flat_atom_name_list(
        present_atom_names, caller=caller, argument="present_atom_names"
    )


def _ph(pH, caller=None):
    if (
        isinstance(pH, Real)
        and not isinstance(pH, (bool, np.bool_))
        and math.isfinite(pH)
    ):
        return float(pH)
    raise ArgumentError("pH", value=pH, caller=caller)


def _boolean(value, name, caller):
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    raise ArgumentError(name, value=value, caller=caller)


def _n_terminal(is_n_terminal, caller=None):
    return _boolean(is_n_terminal, "is_n_terminal", caller)


def _c_terminal(is_c_terminal, caller=None):
    return _boolean(is_c_terminal, "is_c_terminal", caller)


def _disulfide(is_disulfide, caller=None):
    return _boolean(is_disulfide, "is_disulfide", caller)


ARGUMENT_DIGESTERS = dict(
    NAMING_DIGESTERS,
    present_atom_names=_present_atom_names,
    pH=_ph,
    is_n_terminal=_n_terminal,
    is_c_terminal=_c_terminal,
    is_disulfide=_disulfide,
)
