"""Validating an explicit partial-assessment disposition."""

from molsysmt._private.smonitor import ArgumentError


def digest_on_ambiguous(on_ambiguous, caller=None):
    if isinstance(on_ambiguous, str) and on_ambiguous in ("raise", "report"):
        return on_ambiguous
    raise ArgumentError("on_ambiguous", value=on_ambiguous, caller=caller)
