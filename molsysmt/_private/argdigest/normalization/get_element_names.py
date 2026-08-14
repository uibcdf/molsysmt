"""The bare element names accepted by `get`, resolved against its `element` argument.

`msm.get(molsys, element='atom', name=True)` asks for `atom_name`, and the same `name`
asks for `group_name` when the element is a group. One table per element states exactly
which bare names that element accepts.

The public provider enumerates every real combination rather than generating a
Cartesian product. This module only scopes that semantic data to the concrete MolSysMT
caller.
"""

from argdigest import AliasTable
from molsysmt.attribute import get_argument_aliases

_ELEMENT_ALIASES = get_argument_aliases()['element_attribute_aliases']

TABLES = [
    AliasTable(
        applies_to='molsysmt.basic.get.get',
        when={'element': element},
        aliases=aliases,
    )
    for element, aliases in _ELEMENT_ALIASES.items()
]
