from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='openmm.PDBFile')
@dep_digest('openmm')
def to_openmm_PDBFile(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):


    from molsysmt._private.variables import is_all
    import os
    from openmm.app import PDBFile
    from io import StringIO

    if isinstance(item, str):
        is_file = False
        if len(item) < 1024:
            try:
                if os.path.isfile(item):
                    is_file = True
            except Exception:
                pass
        
        if is_file:
            tmp_item = PDBFile(item)
        else:
            tmp_item = PDBFile(StringIO(item))
    elif isinstance(item, os.PathLike):
        tmp_item = PDBFile(str(item))
    else:
        tmp_item = item

    if not (is_all(atom_indices) and is_all(structure_indices)):
        from .extract import extract
        tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, skip_digestion=True)

    return tmp_item
