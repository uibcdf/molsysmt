"""Reject keyword typos before checking the admitted writer effects."""

from argdigest import FunctionContract

contract = FunctionContract(
    caller="molsysviewer_molsysmt._basic.set",
    admits="attribute",
    description="Native attribute names; the adapter separately receives their effects.",
)
