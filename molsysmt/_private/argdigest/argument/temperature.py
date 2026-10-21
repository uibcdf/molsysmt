import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError

functions_with_boolean = (
    "molsysmt.basic.get.get",
    "molsysmt.basic.compare.compare",
    "molsysmt.basic.iterator.__init__",
    "iterators.__init__",
)


def digest_temperature(temperature, caller=None, structure_series=False):
    """Digesting temperature for scalar settings or structural series.

    Parameters
    ----------
    temperature : quantity, bool or None
        Physical value with temperature units, such as K. Boolean flags are
        admitted only by query callers; None denotes an absent value.
    caller : str, optional
        ArgDigest contract key used for query admission and diagnostics.
    structure_series : bool, default=False
        Decorator-owned context at native structure boundaries. Admit a real
        one-dimensional quantity or normalize a scalar to a length-one series.
        Other callers retain the scalar setting contract.

    Returns
    -------
    quantity, bool or None
        Standardized physical value, a query flag, or an absent value.

    Raises
    ------
    ArgumentError
        If units or values do not satisfy the selected context.
    """

    if caller is not None and caller.endswith(functions_with_boolean):
        if isinstance(temperature, bool):
            return temperature

    if temperature is None:
        return temperature

    if structure_series:
        from ._structure_series import digest_structure_series

        return digest_structure_series(temperature, "temperature", {"[K]": 1}, caller)

    value, unit = puw.get_value_and_unit(temperature)

    if not puw.check(unit, dimensionality={"[K]": 1}):
        raise ArgumentError(
            "temperature", value=temperature, caller=caller, message=None
        )

    if isinstance(value, (int, np.int64, float, np.float64)):
        return puw.standardize(puw.quantity(value, unit))

    raise ArgumentError("temperature", value=temperature, caller=caller, message=None)
