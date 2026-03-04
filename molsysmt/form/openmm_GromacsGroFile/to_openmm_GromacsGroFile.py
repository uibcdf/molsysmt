from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='openmm.GromacsGroFile')
@dep_digest('openmm')
def to_openmm_GromacsGroFile(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):


    from molsysmt._private.variables import is_all
    import os

    if isinstance(item, (str, os.PathLike)):
        from openmm.app import GromacsGroFile
        tmp_item = GromacsGroFile(str(item))
    else:
        tmp_item = item

    if not (is_all(atom_indices) and is_all(structure_indices)):
        from .extract import extract
        tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, skip_digestion=True)

    return tmp_item


