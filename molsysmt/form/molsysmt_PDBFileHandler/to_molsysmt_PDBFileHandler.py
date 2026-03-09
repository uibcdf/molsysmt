import os
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.PDBFileHandler')
def to_molsysmt_PDBFileHandler(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    from molsysmt.native.pdb_file_handler import PDBFileHandler
    from molsysmt._private.variables import is_all

    if isinstance(item, str):
        is_file = False
        if len(item) < 1024:
            try:
                if os.path.isfile(item):
                    is_file = True
            except:
                pass
        
        if is_file:
            tmp_item = PDBFileHandler(item)
        else:
            tmp_item = PDBFileHandler(item) # PDBFileHandler will handle it as string text
    elif isinstance(item, os.PathLike):
        tmp_item = PDBFileHandler(str(item))
    else:
        tmp_item = item

    if not (is_all(atom_indices) and is_all(structure_indices)):
        from .extract import extract
        tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, 
                           copy_if_all=copy_if_all, skip_digestion=True)

    return tmp_item
