from argdigest import Domain

from molsysmt._private.attribute_catalog import attributes

# Several public functions take attribute names as boolean keywords -- `msm.get(molsys,
# n_atoms=True)` -- and there are more than a hundred of them, so they can never be
# signature parameters. This domain points at the catalogue instead of copying it, so
# the two cannot drift apart.
domain = Domain(
    name="attribute",
    contains=attributes.__contains__,
    members=lambda: tuple(attributes),
    description="canonical MolSysMT attribute names",
)
