from molsysmt._private.digestion import arg_digest

@arg_digest(form='file:prmtop')
def to_openmm_AmberPrmtopFile(item, atom_indices='all', skip_digestion=False):

    from openmm.app import AmberPrmtopFile

    tmp_item = AmberPrmtopFile(item)

    return tmp_item

