"""Contract for `get_neighbors`, whose two search criteria exclude each other.

`get_neighbors` searches either within a distance (`threshold`) or by count
(`n_neighbors`), and the two are alternatives: the implementation has one branch for each
and rejects anything else. Declaring it here moves the rule out of the function body and
makes it fail before any work is done, with a catalogued diagnostic that names both
arguments.

The runtime check stays: it also covers an explicit `threshold=None`, which is *supplied*
as far as the contract is concerned but carries no criterion.
"""

from argdigest import FunctionContract

contract = FunctionContract(
    caller='molsysmt.structure.get_neighbors.get_neighbors',
    mutually_exclusive=[('threshold', 'n_neighbors')],
    requires_any_of=['threshold', 'n_neighbors'],
    description='Searches by distance or by count, never both and never neither.',
)
