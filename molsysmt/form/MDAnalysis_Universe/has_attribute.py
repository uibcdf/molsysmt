from molsysmt._private.argdigest import arg_digest

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
    elif output and not include_none and attribute in {
        'coordinates', 'velocities', 'box', 'time', 'structure_id',
        'structure_index', 'n_structures',
    }:
        trajectory = getattr(molecular_system, 'trajectory', None)
        output = trajectory is not None
        if output and attribute == 'velocities':
            output = bool(getattr(trajectory.ts, 'has_velocities', False))
        elif output and attribute == 'box':
            dimensions = getattr(trajectory.ts, 'dimensions', None)
            output = dimensions is not None and not __import__('numpy').allclose(
                dimensions[:3], 0.0
            )
        elif output and attribute == 'time':
            from .get_structural_attributes import _timestep_has_time

            output = _timestep_has_time(trajectory.ts)

    return bool(output)
