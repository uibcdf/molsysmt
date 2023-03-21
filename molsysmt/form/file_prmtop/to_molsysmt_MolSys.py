from molsysmt._private.digestion import digest

@digest(form='file:prmtop')
def to_molsysmt_MolSys(item, atom_indices='all',
        component_id=None, component_type=None, component_name=None,
        entity_id=None, entity_type=None, entity_name=None,
        structure_id=None, coordinates=None, velocities=None, time=None, box=None,
        formal_charge=None, partial_charge=None, forcefield=None, non_bonded_method=None,
        cutoff_distance=None, switch_distance=None, dispersion_correction=None, ewald_error_tolerance=None,
        hydrogen_mass=None, constraints=None, flexible_constraints=None, water_model=None, rigid_water=None,
        implicit_solvent=None, solute_dielectric=None, solvent_dielectric=None, salt_concentration=None,
        kappa=None):

    from molsysmt.native import MolSys, Structures
    from .to_molsysmt_Topology import to_molsysmt_Topology
    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices)
    tmp_item.structures = Structures()
    tmp_item.structures.append_structures(coordinates=coordinates)

    return tmp_item

