"""Contracts for the public functions that take attribute names through `**kwargs`.

These five cannot declare their arguments in a signature: they accept the whole
attribute catalogue as boolean keywords, and there are 118 of them. Pointing at the
`attribute` domain keeps one source of truth and makes a mistyped attribute name fail
where it happens instead of deep inside `get`.

None of them declares `requires_any_of`. A call with no attribute at all is meaningful
in `contains` and `is_composed_of` -- both implement an explicit branch for it -- so
requiring one would break documented behaviour.
"""

from argdigest import FunctionContract

CONTRACTS = [
    FunctionContract(
        caller='molsysmt.basic.get.get',
        admits='attribute',
        description='Attributes are requested as boolean keywords.',
    ),
    FunctionContract(
        caller='molsysmt.basic.set.set',
        admits='attribute',
        description='Attributes are assigned as keywords.',
    ),
    FunctionContract(
        caller='molsysmt.basic.contains.contains',
        admits='attribute',
        description='Attribute conditions as attribute=value pairs.',
    ),
    FunctionContract(
        caller='molsysmt.basic.is_composed_of.is_composed_of',
        admits='attribute',
        description='Composition conditions as attribute=value pairs.',
    ),
    FunctionContract(
        caller='molsysmt.basic.compare.compare',
        admits='attribute',
        description='Attributes to compare, as keyword booleans.',
    ),
]
