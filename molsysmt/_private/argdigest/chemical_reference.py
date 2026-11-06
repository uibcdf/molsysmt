"""Validate reference identity and explicitly selected acquisition/chemistry policy."""

import re
from pathlib import Path

import numpy as np

from molsysmt._private.smonitor import ArgumentChoiceError, ArgumentError

from .argument.skip_digestion import digest_skip_digestion

DIGEST_OPTIONS = {
    "digestion_source": "molsysmt._private.argdigest.chemical_reference",
    "digestion_style": "registry",
    "strictness": "error",
}


def _component_id(value, caller=None):
    if not isinstance(value, str) or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9_.+-]*", value
    ):
        raise ArgumentError("component_id", value=value, caller=caller)
    return value.upper()


def _source(value, caller=None):
    if isinstance(value, bytes) and value or isinstance(value, Path):
        return value
    if isinstance(value, str) and value and "\x00" not in value:
        return "rcsb" if value.lower() == "rcsb" else Path(value)
    raise ArgumentError("source", value=type(value).__name__, caller=caller)


def _choice(value, choices, argument, caller):
    if not isinstance(value, str) or value not in choices:
        raise ArgumentChoiceError(argument, value, choices, caller=caller)
    return value


def _method(value, caller=None):
    return _choice(value, ["ccd_tables", "ccd_canonical_descriptor"], "method", caller)


def _hydrogen_policy(value, caller=None):
    return _choice(
        value, ["explicit_atoms", "stored_counts"], "hydrogen_policy", caller
    )


def _descriptor_program(value, caller=None):
    if not isinstance(value, str) or not value.strip():
        raise ArgumentError("descriptor_program", value=value, caller=caller)
    return value


def _max_matches(value, caller=None):
    if (
        isinstance(value, (int, np.integer))
        and not isinstance(value, (bool, np.bool_))
        and value > 0
    ):
        return int(value)
    raise ArgumentError("max_matches", value=value, caller=caller)


ARGUMENT_DIGESTERS = dict(
    component_id=_component_id,
    source=_source,
    method=_method,
    hydrogen_policy=_hydrogen_policy,
    descriptor_program=_descriptor_program,
    max_matches=_max_matches,
    skip_digestion=digest_skip_digestion,
)
