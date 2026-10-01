"""Validate a nonempty ordered collection of SMARTS expressions."""

from molsysmt._private.smonitor import ArgumentError


def digest_patterns(patterns, caller=None):
    if isinstance(patterns, str):
        patterns = (patterns,)
    if isinstance(patterns, (list, tuple)) and patterns and all(isinstance(p, str) and p.strip() for p in patterns):
        return tuple(patterns)
    raise ArgumentError("patterns", value=patterns, caller=caller)
