from molsysmt._private.digestion import digest

@digest(form='mdtraj.Topology')
def to_openmm_Topology(item, atom_indices='all'):

    from ..openmm_Topology import extract as extract_openmm_Topology

    tmp_item = item.to_openmm()
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices, copy_if_all=False)

    return tmp_item

def _to_openmm_Topology(item, atom_indices='all', structure_indices='all'):

    return to_openmm_Topology(item, atom_indices=atom_indices)

