from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSysOld')
def to_openmm_Context(item, atom_indices='all', structure_indices='all',
        forcefield='AMBER14', water_model=None, implicit_solvent=None,
        non_bonded_method='no cutoff', constraints='hbonds', switch_distance=None,
        dispersion_correction=False, ewald_error_tolerance=0.0005,
        integrator='Langevin', temperature='300.0 kelvin', friction='1.0/picoseconds', time_step='2 femtoseconds',
        platform='CUDA'):

    from . import to_openmm_Topology
    from . import get_coordinates_from_atom
    from ..openmm_Topology import to_openmm_Context as openmm_Topology_to_openmm_Context

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices)

    tmp_item = openmm_Topology_to_openmm_Context(tmp_item, coordinates=coordinates,
            forcefield=forcefield, water_model=water_model, implicit_solvent=implicit_solvent,
            non_bonded_method=non_bonded_method, constraints=constraints, switch_distance=switch_distance,
            dispersion_correction=dispersion_correction, ewald_error_tolerance=ewald_error_tolerance,
            integrator=integrator, temperature=temperature, friction=friction, time_step=time_step,
            platform=platform)

    return tmp_item

