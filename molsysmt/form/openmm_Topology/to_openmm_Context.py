from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_openmm_Context(item, atom_indices='all', coordinates=None, forcefield='AMBER14', water_model=None,
        implicit_solvent=None, non_bonded_method='no cutoff', constraints='hbonds', switch_distance=None,
        dispersion_correction=False, ewald_error_tolerance=0.0005, integrator='Langevin', temperature=None,
        friction='1.0/picoseconds', time_step='2 femtoseconds', platform='CUDA', skip_digestion=False):


    from . import to_openmm_System
    from ..openmm_System import to_openmm_Context as openmm_System_to_openmm_Context

    system = to_openmm_System(item, atom_indices=atom_indices, forcefield=forcefield,
            water_model=water_model, implicit_solvent=implicit_solvent,
            non_bonded_method=non_bonded_method, constraints=constraints,
            switch_distance=switch_distance, dispersion_correction=dispersion_correction,
            ewald_error_tolerance=ewald_error_tolerance, skip_digestion=True)
    context = openmm_System_to_openmm_Context(system, coordinates=coordinates,
            integrator=integrator, temperature=temperature, friction=friction,
            time_step=time_step, platform=platform, skip_digestion=True)

    return context

