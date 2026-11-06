"""Bound the synchronous configuration keyword domain without generic value coercion."""

from argdigest import FunctionContract

CONTRACTS = [
    FunctionContract(caller="molsysmt.configure.context", admits="configuration"),
    FunctionContract(caller="molsysmt.configure.__init__", admits="configuration"),
]
