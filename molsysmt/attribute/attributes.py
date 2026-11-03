"""Expose the shared catalog without owning a second mutable registry.

Decorator declarations load the internal data directly to avoid importing this
package's decorated public query helpers while their registry is being built.
"""

from molsysmt._private.attribute_catalog import add_attribute as _add_attribute
from molsysmt._private.attribute_catalog import attribute_synonyms as attribute_synonyms
from molsysmt._private.attribute_catalog import attributes as attributes
from molsysmt._private.attribute_catalog import (
    chemical_state_attributes as chemical_state_attributes,
)
from molsysmt._private.attribute_catalog import (
    independent_attributes as independent_attributes,
)
from molsysmt._private.attribute_catalog import (
    mechanical_attributes as mechanical_attributes,
)
from molsysmt._private.attribute_catalog import (
    structural_attributes as structural_attributes,
)
from molsysmt._private.attribute_catalog import (
    topological_attributes as topological_attributes,
)


def add_attribute(
    name,
    synonyms=None,
    depends_on=None,
    dependants=None,
    runs_on_elements=False,
    runs_on_structures=False,
    topological=False,
    structural=False,
    mechanical=False,
    chemical_state=False,
    dynamical=False,
    get_from=None,
    set_to=None,
    values=None,
    domain=None,
    dtype=None,
    nullable=None,
    units=None,
):
    """Registering metadata through the existing catalog-builder entry point."""
    return _add_attribute(
        name,
        synonyms=synonyms,
        depends_on=depends_on,
        dependants=dependants,
        runs_on_elements=runs_on_elements,
        runs_on_structures=runs_on_structures,
        topological=topological,
        structural=structural,
        mechanical=mechanical,
        chemical_state=chemical_state,
        dynamical=dynamical,
        get_from=get_from,
        set_to=set_to,
        values=values,
        domain=domain,
        dtype=dtype,
        nullable=nullable,
        units=units,
    )
