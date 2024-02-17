from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSysOld')
def to_openmm_System(item, atom_indices='all', structure_indices='all',
        forcefield='AMBER14', water_model=None, implicit_solvent=None,
        non_bonded_method='no cutoff', constraints='hbonds', switch_distance=None,
        dispersion_correction=False, ewald_error_tolerance=0.0005, skip_digestion=False):

    from . import to_openmm_Topology
    from ..openmm_Topology import to_openmm_System as openmm_Topology_to_openmm_System

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    system = to_openmm_System(tmp_item, forcefield=forcefield,
            water_model=water_model, implicit_solvent=implicit_solvent,
            non_bonded_method=non_bonded_method, constraints=constraints,
            switch_distance=switch_distance, dispersion_correction=dispersion_correction,
            ewald_error_tolerance=ewald_error_tolerance, skip_digestion=True)

    return tmp_item

