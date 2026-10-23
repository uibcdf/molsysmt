"""Validating an explicit format constraint independently of an output form."""

from molsysmt._private.smonitor import ArgumentError

from .to_form import digest_to_form


def digest_target_form(target_form, caller=None):
    try:
        return digest_to_form(target_form, caller=caller)
    except ArgumentError:
        raise ArgumentError("target_form", value=target_form, caller=caller) from None
