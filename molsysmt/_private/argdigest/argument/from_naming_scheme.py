"""Validate an explicit source naming vocabulary without choosing a default."""


def digest_from_naming_scheme(from_naming_scheme, caller=None):
    from molsysmt._private.argdigest.name_resolution import _scheme
    from molsysmt._private.smonitor import ArgumentChoiceError
    from molsysmt.native._group_naming import NAMES

    try:
        return _scheme(from_naming_scheme, caller=caller)
    except ArgumentChoiceError as error:
        raise ArgumentChoiceError(
            "from_naming_scheme",
            value=from_naming_scheme,
            choices=list(NAMES),
            caller=caller,
        ) from error
