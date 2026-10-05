"""Validating portable historical records without asserting source authenticity."""

from molsysmt._private.preparation_history import encode_history
from molsysmt._private.smonitor import ArgumentError


def digest_preparation_history(preparation_history, caller=None):
    try:
        encode_history(preparation_history, copy_arrays=False)
    except (ValueError, TypeError) as error:
        raise ArgumentError(
            "preparation_history",
            value=preparation_history,
            caller=caller,
            message=str(error),
        ) from error
    return preparation_history
