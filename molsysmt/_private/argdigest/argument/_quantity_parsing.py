from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError


def parse_quantity_string(argument, value, caller=None):
    """Parse a string into a quantity, refusing at the boundary when it does not parse.

    Without this, an unparseable string leaves the digester as the unit registry's own
    exception, so the same class of bad input reaches the caller as two different
    exception types depending on whether it was written as a string or as a bare number,
    and the one that escapes names pint rather than the argument.
    """

    try:
        return puw.parse.parse(value)
    except Exception as error:
        raise ArgumentError(argument, value=value, caller=caller, cause=error) from error
