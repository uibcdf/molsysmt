"""Reuse native criterion admission before bound defaults are forwarded."""

from dataclasses import replace

from molsysmt._private.argdigest.function.structure_get_neighbors import (
    contract as _native_contract,
)

contract = replace(
    _native_contract, caller="molsysviewer_molsysmt._structure.get_neighbors"
)
