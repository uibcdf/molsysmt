from molsysmt._private.digestion import digest
from molsysmt.dependencies import requires

@digest(form='openmm.AmberPrmtopFile')
@requires('openmm')
def to_openmm_AmberPrmtopFile(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, skip_digestion=True)

