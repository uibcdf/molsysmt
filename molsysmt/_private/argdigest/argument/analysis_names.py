"""Validate H5MSM interaction-analysis name selectors."""

from argdigest.core.caller import caller_matches

from molsysmt._private.smonitor import ArgumentError


def digest_analysis_names(analysis_names, caller=None):
    if not caller_matches(caller, "read_layers") or analysis_names is None:
        return analysis_names
    if isinstance(analysis_names, str):
        values = [analysis_names]
    elif isinstance(analysis_names, (list, tuple)):
        values = analysis_names
    else:
        raise ArgumentError("analysis_names", value=analysis_names, caller=caller)
    if any(not isinstance(value, str) or not value for value in values):
        raise ArgumentError("analysis_names", value=analysis_names, caller=caller)
    return analysis_names
