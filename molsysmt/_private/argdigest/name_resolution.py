"""Validate scalar name interpretation independently of molecular forms."""

from molsysmt._private.smonitor import ArgumentChoiceError, ArgumentError

from .argument.skip_digestion import digest_skip_digestion

DIGEST_OPTIONS = {
    "digestion_source": "molsysmt._private.argdigest.name_resolution",
    "digestion_style": "registry",
    "strictness": "error",
}


def _name(name, caller=None):
    if isinstance(name, str) and name:
        return name
    raise ArgumentError("name", value=name, caller=caller)


def _scheme(naming_scheme, caller=None):
    from molsysmt.native._group_naming import NAMES

    if (
        naming_scheme is None
        or isinstance(naming_scheme, str)
        and naming_scheme in NAMES
    ):
        return naming_scheme
    raise ArgumentChoiceError(
        "naming_scheme", value=naming_scheme, choices=list(NAMES), caller=caller
    )


def _group_name(group_name, caller=None):
    # Missing labels are a supported recognition input, never an invented name.
    import pandas as pd

    if group_name is None or isinstance(group_name, str) and group_name:
        return group_name
    if pd.api.types.is_scalar(group_name) and pd.isna(group_name):
        return group_name
    raise ArgumentError("group_name", value=group_name, caller=caller)


ARGUMENT_DIGESTERS = {
    "name": _name,
    "group_name": _group_name,
    "naming_scheme": _scheme,
    "skip_digestion": digest_skip_digestion,
}
