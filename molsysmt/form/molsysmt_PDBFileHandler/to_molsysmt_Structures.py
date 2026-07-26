import os
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.PDBFileHandler')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler
    from .to_molsysmt_MolSys import _build_structures_from_content

    if isinstance(item, (str, os.PathLike)):
        item = to_molsysmt_PDBFileHandler(str(str(item)), skip_digestion=True)
        opened_here = True
    else:
        opened_here = False

    tmp_item = _build_structures_from_content(item)
    tmp_item = tmp_item.extract(atom_indices=atom_indices, structure_indices=structure_indices,
                                copy_if_all=False, skip_digestion=True)

    if opened_here:
        item.close()

    return tmp_item
