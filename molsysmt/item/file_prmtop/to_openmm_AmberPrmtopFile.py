from molsysmt._private.digestion import digest

@digest(form='file:prmtop')
def to_openmm_AmberPrmtopFile(item, atom_indices='all'):

    from openmm.app import AmberPrmtopFile

    tmp_item = AmberPrmtopFile(item)

    return tmp_item

