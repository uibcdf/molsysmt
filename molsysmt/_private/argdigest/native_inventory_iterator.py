"""Reuse native query flag contracts at native inventory iterator boundaries."""

from importlib import import_module

from argdigest import AliasTable, FunctionContract

from molsysmt._private.attribute_aliases import get_alias_contract

from .native_queries import ARGUMENT_DIGESTERS as _QUERY_DIGESTERS

CONTRACTS = [FunctionContract(caller_pattern="*.__init__", admits="attribute")]
_ALIASES = get_alias_contract()
TABLES = [AliasTable(applies_to="*.__init__", aliases=_ALIASES["attribute_synonyms"])]
TABLES.extend(
    AliasTable(applies_to="*.__init__", when={"element": element}, aliases=aliases)
    for element, aliases in _ALIASES["element_attribute_aliases"].items()
)
ARGUMENT_DIGESTERS = dict(_QUERY_DIGESTERS)
for _name in ("molecular_system", "indices", "start", "stop", "step", "chunk"):
    _module = import_module("molsysmt._private.argdigest.argument." + _name)
    ARGUMENT_DIGESTERS[_name] = getattr(_module, "digest_" + _name)
