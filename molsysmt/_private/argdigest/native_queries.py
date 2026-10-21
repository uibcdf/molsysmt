"""Reuse basic query value contracts at native method boundaries.

ArgDigest still owns binding, aliases and keyword-domain enforcement under the
actual native caller. Value digesters receive the existing basic provider's
context, so native queries do not acquire a second set of attribute flag rules.
The registry interface is a supported ArgDigest discovery mechanism.
"""

from functools import wraps
from importlib import import_module
from inspect import signature

from argdigest import AliasTable, FunctionContract

from molsysmt.attribute import attributes, get_argument_aliases

# These wildcard rules belong only to the native methods' decorator plan.
# Universal functions and unrelated APIs keep their own scoped registrations.
CONTRACTS = [FunctionContract(caller_pattern="*.get", admits="attribute")]
_ALIASES = get_argument_aliases()
TABLES = [AliasTable(applies_to="*.get", aliases=_ALIASES["attribute_synonyms"])]
TABLES.extend(
    AliasTable(applies_to="*.get", when={"element": element}, aliases=aliases)
    for element, aliases in _ALIASES["element_attribute_aliases"].items()
)


def _query_value_contract(function):
    accepts_caller = "caller" in signature(function).parameters

    @wraps(function)
    def digest(*args, **kwargs):
        if accepts_caller:
            caller = kwargs.get("caller")
            kwargs["caller"] = (
                "molsysmt.basic.info.info"
                if isinstance(caller, str) and caller.endswith(".info")
                else "molsysmt.basic.get.get"
            )
        return function(*args, **kwargs)

    return digest


ARGUMENT_DIGESTERS = {}
for _name in set(attributes) | {
    "element",
    "selection",
    "structure_indices",
    "mask",
    "syntax",
    "get_missing_bonds",
    "output_type",
    "chemical_state",
    "skip_digestion",
}:
    _path = "molsysmt._private.argdigest.argument." + _name
    try:
        _module = import_module(_path)
    except ModuleNotFoundError as _error:
        if _error.name != _path:
            raise
        continue
    _function = getattr(_module, "digest_" + _name, None)
    if _function is not None:
        ARGUMENT_DIGESTERS[_name] = _query_value_contract(_function)
