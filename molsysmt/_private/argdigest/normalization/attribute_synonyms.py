"""The attribute synonyms, scoped to the functions that take attribute names.

`molsysmt.attribute.get_argument_aliases()` is the source of truth. These tables scope
its semantic data to the public functions that accept attribute names.

**The scope is not incidental.** These synonyms rename attribute *names*, and only three
public functions take attribute names as keywords. Everywhere else the same words are
ordinary parameters: `atom_indices` is a real parameter of every form adapter, and a
global table would rename it to `atom_index`, which no adapter declares. Declaring these
globally breaks 76 tests, which is how the scope was rediscovered.
"""

from argdigest import AliasTable

from molsysmt.attribute import get_argument_aliases

#: The public functions whose keywords are attribute names.
_ATTRIBUTE_TAKING_CALLERS = (
    'molsysmt.basic.get.get',
    'molsysmt.basic.contains.contains',
    'molsysmt.basic.is_composed_of.is_composed_of',
)

_ALIASES = get_argument_aliases()['attribute_synonyms']

TABLES = [
    AliasTable(
        applies_to=caller,
        aliases=_ALIASES,
        description='plural and anatomical synonyms of the canonical attribute names',
    )
    for caller in _ATTRIBUTE_TAKING_CALLERS
]
