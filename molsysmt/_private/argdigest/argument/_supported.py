"""Shared validation for the bounded capability-report filters."""

from molsysmt._private.smonitor import ArgumentChoiceError, ArgumentError


def choice(value, name, choices, caller):
    if (value is None or isinstance(value, str)) and value in choices:
        return value
    raise ArgumentChoiceError(name, value, choices, caller=caller)


def form_filter(value, name, caller):
    if value is None or isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)) and all(isinstance(v, str) for v in value):
        return list(value)
    raise ArgumentError(name, value=value, caller=caller)
