"""The bare element names accepted by `get`, resolved against its `element` argument.

`msm.get(molsys, element='atom', name=True)` asks for `atom_name`, and the same `name`
asks for `group_name` when the element is a group. One table per element states exactly
which bare names that element accepts.

They are written out rather than generated from a `{element}_{name}` template, and the
difference is not verbosity. Several combinations do not exist -- there is no
`atom_order`, `chain_order` or `bond_name` -- and a template would have accepted them,
producing an attribute name nothing defines and an error much further downstream. The
tables below were derived from the element list in `molsysmt.element` crossed with the
attribute catalogue, so they contain every combination that is real and none that is not.
"""

from argdigest import AliasTable

TABLES = [
    AliasTable(
        applies_to='molsysmt.basic.get.get',
        when={'element': 'atom'},
        aliases={'name': 'atom_name',
                 'index': 'atom_index',
                 'id': 'atom_id',
                 'type': 'atom_type'},
    ),
    AliasTable(
        applies_to='molsysmt.basic.get.get',
        when={'element': 'group'},
        aliases={'name': 'group_name',
                 'index': 'group_index',
                 'id': 'group_id',
                 'type': 'group_type'},
    ),
    AliasTable(
        applies_to='molsysmt.basic.get.get',
        when={'element': 'component'},
        aliases={'name': 'component_name',
                 'index': 'component_index',
                 'id': 'component_id',
                 'type': 'component_type'},
    ),
    AliasTable(
        applies_to='molsysmt.basic.get.get',
        when={'element': 'molecule'},
        aliases={'name': 'molecule_name',
                 'index': 'molecule_index',
                 'id': 'molecule_id',
                 'type': 'molecule_type'},
    ),
    AliasTable(
        applies_to='molsysmt.basic.get.get',
        when={'element': 'chain'},
        aliases={'name': 'chain_name',
                 'index': 'chain_index',
                 'id': 'chain_id',
                 'type': 'chain_type'},
    ),
    AliasTable(
        applies_to='molsysmt.basic.get.get',
        when={'element': 'entity'},
        aliases={'name': 'entity_name',
                 'index': 'entity_index',
                 'id': 'entity_id',
                 'type': 'entity_type'},
    ),
    AliasTable(
        applies_to='molsysmt.basic.get.get',
        when={'element': 'bond'},
        aliases={'index': 'bond_index',
                 'id': 'bond_id',
                 'type': 'bond_type',
                 'order': 'bond_order'},
    ),
]
