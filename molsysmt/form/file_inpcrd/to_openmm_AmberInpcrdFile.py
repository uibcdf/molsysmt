from molsysmt._private.digestion import digest

@digest(form='file:inpcrd')
def to_openmm_AmberInpcrdFile(item, atom_indices='all', structure_indices='all', digest=False):

    from openmm.app import AmberInpcrdFile

    tmp_item = AmberInpcrdFile(item)

    return tmp_item

