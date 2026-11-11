"""Validate the explicit modular H5MSM output version."""

from argdigest.core.caller import caller_matches

from molsysmt._private.h5msm_storage.versions import MODULAR_VERSIONS
from molsysmt._private.smonitor import ArgumentChoiceError


def digest_format_version(format_version, caller=None):
    # None retains the existing direct file adapter's legacy copy route.
    if format_version is None and caller_matches(
        caller, "molsysmt.form.file_h5msm.to_file_h5msm.to_file_h5msm"
    ):
        return None
    if isinstance(format_version, str) and format_version in MODULAR_VERSIONS:
        return format_version
    raise ArgumentChoiceError(
        "format_version", format_version, sorted(MODULAR_VERSIONS), caller=caller
    )
