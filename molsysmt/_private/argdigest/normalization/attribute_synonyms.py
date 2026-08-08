"""The attribute synonyms, scoped to the functions that take attribute names.

`molsysmt.attribute._attribute_synonyms` is the source of truth; this points at it rather
than copying, so the two cannot drift apart.

**The scope is not incidental.** These synonyms rename attribute *names*, and only three
public functions take attribute names as keywords. Everywhere else the same words are
ordinary parameters: `atom_indices` is a real parameter of every form adapter, and a
global table would rename it to `atom_index`, which no adapter declares. Declaring these
globally breaks 76 tests, which is how the scope was rediscovered.
"""

from argdigest import AliasTable

from molsysmt.attribute import _attribute_synonyms

#: The public functions whose keywords are attribute names.
_ATTRIBUTE_TAKING_CALLERS = (
    'molsysmt.basic.get.get',
    'molsysmt.basic.contains.contains',
    'molsysmt.basic.is_composed_of.is_composed_of',
)

TABLES = [
    AliasTable(
        applies_to=caller,
        aliases=dict(_attribute_synonyms),
        description='plural and anatomical synonyms of the canonical attribute names',
    )
    for caller in _ATTRIBUTE_TAKING_CALLERS
]
