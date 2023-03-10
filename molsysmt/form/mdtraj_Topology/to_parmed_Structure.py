from molsysmt._private.digestion import digest

@digest(form='mdtraj.Topology')
def to_parmed_Structure(item, atom_indices='all'):

    from . import to_openmm_Topology
    from .openmm_Topology import to_parmed_Structure as openmm_Topology_to_parmed_Structure

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices)
    tmp_item = openmm_Topology_to_parmed_Structure(tmp_item)

    return tmp_item

