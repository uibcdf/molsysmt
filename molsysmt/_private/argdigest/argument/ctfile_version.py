from molsysmt._private.smonitor import ArgumentChoiceError


def digest_ctfile_version(ctfile_version, caller=None):
    """Validating the explicitly requested CTAB syntax."""
    if isinstance(ctfile_version, str) and ctfile_version in {"V2000", "V3000"}:
        return ctfile_version
    raise ArgumentChoiceError(
        "ctfile_version", ctfile_version, ["V2000", "V3000"], caller=caller
    )
