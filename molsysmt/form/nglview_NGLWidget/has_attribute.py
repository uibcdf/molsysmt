from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='nglview.NGLWidget')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):

    from molsysmt.attribute import attributes as all_attributes

    attribute_info = all_attributes[attribute]

    if attribute_info['topological']:
        from ._topology_sidecar import get_topology_sidecar

        topology = get_topology_sidecar(molecular_system)
        if topology is None:
            if attribute in {'bond_id', 'bond_order', 'bond_type'}:
                return False
            try:
                from .to_molsysmt_Topology import to_molsysmt_Topology

                topology = to_molsysmt_Topology(
                    molecular_system,
                    get_missing_bonds=False,
                    skip_digestion=True,
                )
            except (AttributeError, IndexError, KeyError, ValueError):
                return False
        from molsysmt.form.molsysmt_Topology.has_attribute import (
            has_attribute as topology_has_attribute,
        )

        return topology_has_attribute(
            topology,
            attribute,
            include_none=include_none,
            skip_digestion=True,
        )

    if attribute_info['structural']:
        try:
            from .to_molsysmt_Structures import to_molsysmt_Structures

            structures = to_molsysmt_Structures(
                molecular_system,
                skip_digestion=True,
            )
        except (AttributeError, IndexError, KeyError, ValueError):
            return False
        from molsysmt.form.molsysmt_Structures.has_attribute import (
            has_attribute as structures_has_attribute,
        )

        return structures_has_attribute(
            structures,
            attribute,
            include_none=include_none,
            skip_digestion=True,
        )

    return False
