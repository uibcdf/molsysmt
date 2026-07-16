from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='MDAnalysis.Universe')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):

    from . import attributes

    output = attributes[attribute]

    if output and not include_none and attribute in {
        'formal_charge', 'bond_type', 'bond_order', 'fractional_bond_order',
        'bond_is_aromatic', 'bond_evidence', 'connectivity_completeness',
    }:
        from molsysmt.form.MDAnalysis_Topology.has_attribute import (
            has_attribute as topology_has_attribute,
        )

        output = topology_has_attribute(
            molecular_system._topology,
            attribute,
            include_none=False,
            skip_digestion=True,
        )

    return bool(output)
