from molsysmt._private.digestion import digest

@digest(form='file:inpcrd')
def to_openmm_AmberInpcrdFile(item, atom_indices='all', structure_indices='all'):

    from openmm.app import AmberInpcrdFile

    tmp_item = AmberInpcrdFile(item)

    return tmp_item

def _to_openmm_AmberInpcrdFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_openmm_AmberInpcrdFile(item, atom_indices=atom_indices, structure_indices=structure_indices)
