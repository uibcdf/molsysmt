"""Validate a finite, positive number of bounded placement attempts."""


def digest_max_attempts(max_attempts, caller=None):
    from molsysmt._private.smonitor import ArgumentError
    from molsysmt.build._ion_replacement import nonnegative_integer

    value = nonnegative_integer(max_attempts, "max_attempts", caller=caller)
    if value == 0:
        raise ArgumentError(
            "max_attempts",
            value=value,
            caller=caller,
            message="At least one placement attempt is required.",
        )
    return value
