"""Build alias declarations without importing decorated public query helpers."""

from copy import deepcopy

from .attribute_catalog import attribute_synonyms

_ELEMENT_ATTRIBUTE_ALIASES = {
    "atom": {
        "name": "atom_name",
        "index": "atom_index",
        "id": "atom_id",
        "type": "atom_type",
    },
    "group": {
        "name": "group_name",
        "index": "group_index",
        "id": "group_id",
        "type": "group_type",
    },
    "component": {
        "name": "component_name",
        "index": "component_index",
        "id": "component_id",
        "type": "component_type",
    },
    "molecule": {
        "name": "molecule_name",
        "index": "molecule_index",
        "id": "molecule_id",
        "type": "molecule_type",
    },
    "chain": {
        "name": "chain_name",
        "index": "chain_index",
        "id": "chain_id",
        "type": "chain_type",
    },
    "entity": {
        "name": "entity_name",
        "index": "entity_index",
        "id": "entity_id",
        "type": "entity_type",
    },
    "bond": {
        "index": "bond_index",
        "id": "bond_id",
        "type": "bond_type",
        "order": "bond_order",
    },
}


def get_alias_contract():
    """Return an independent copy of the shared semantic alias declarations."""
    return deepcopy(
        {
            "schema_version": 1,
            "attribute_synonyms": dict(attribute_synonyms),
            "element_attribute_aliases": _ELEMENT_ATTRIBUTE_ALIASES,
        }
    )
