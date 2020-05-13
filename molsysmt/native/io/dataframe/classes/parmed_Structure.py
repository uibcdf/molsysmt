def from_parmed_Structure(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_parmed_Structure import to_openmm_Topology as parmed_Structure_to_openmm_Topology
    from .openmm_Topology import from_openmm_Topology as openmm_Topology_to_molsysmt_DataFrame
    tmp_item = parmed_Structure_to_openmm_Topology(item)
    tmp_item = openmm_Topology_to_molsysmt_DataFrame(tmp_item)
    return tmp_item

