"""Validating a molecular-system template without interpreting its chemistry."""

from molsysmt._private.molecular_system_validation import (
    validate_molecular_system_argument,
)

from .molecular_system import normalize_molecular_system_paths


def digest_template(template, caller=None):
    return validate_molecular_system_argument(
        normalize_molecular_system_paths(template), argument="template", caller=caller
    )
