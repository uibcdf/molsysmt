"""The bare element names accepted by `get`, resolved against its `element` argument.

`msm.get(molsys, element='atom', name=True)` asks for `atom_name`, and the same `name`
asks for `group_name` when the element is a group. One table per element states exactly
which bare names that element accepts.

The shared declaration provider enumerates every real combination rather than
generating a Cartesian product. This module scopes the same public semantic data
to the concrete caller without bootstrapping decorated public query helpers.
"""

from argdigest import AliasTable

from molsysmt._private.attribute_aliases import get_alias_contract

_ELEMENT_ALIASES = get_alias_contract()["element_attribute_aliases"]

TABLES = [
    AliasTable(
        applies_to="molsysmt.basic.get.get",
        when={"element": element},
        aliases=aliases,
    )
    for element, aliases in _ELEMENT_ALIASES.items()
]
