from molsysmt._private.arg_digestion import arg_digest


@arg_digest(form="molsysmt.MolSysBuilder")
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    """Checking instance-aware attribute availability in an editable builder."""

    from .attributes import attributes
    from molsysmt.form.molsysmt_Structures.attributes import (
        attributes as structural_attributes,
    )
    from molsysmt.form.molsysmt_Structures.has_attribute import (
        has_attribute as structures_has_attribute,
    )
    from molsysmt.form.molsysmt_Topology.attributes import (
        attributes as topological_attributes,
    )
    from molsysmt.form.molsysmt_Topology.has_attribute import (
        has_attribute as topology_has_attribute,
    )

    if not attributes[attribute]:
        return False
    if topological_attributes[attribute]:
        return topology_has_attribute(
            molecular_system.topology,
            attribute,
            include_none=include_none,
            skip_digestion=True,
        )
    if structural_attributes[attribute]:
        return structures_has_attribute(
            molecular_system.structures,
            attribute,
            include_none=include_none,
            skip_digestion=True,
        )
    return False
