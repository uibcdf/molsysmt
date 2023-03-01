from molsysmt._private.digestion import digest

@digest(form='file:prmtop')
def to_openmm_AmberPrmtopFile(item, atom_indices='all'):

    from openmm.app import AmberPrmtopFile

    tmp_item = AmberPrmtopFile(item)

    return tmp_item

def _to_openmm_AmberPrmtopFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_nglview_NGLWidget(item, atom_indices=atom_indices)

