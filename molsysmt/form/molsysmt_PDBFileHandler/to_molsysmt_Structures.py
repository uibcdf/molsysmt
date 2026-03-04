import os
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.PDBFileHandler')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import Structures
    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler

    if isinstance(item, (str, os.PathLike)):
        item = to_molsysmt_PDBFileHandler(str(str(item)), skip_digestion=True)
        opened_here = True
    else:
        opened_here = False

    from molsysmt.form.openmm_PDBFile import to_molsysmt_Structures as openmm_PDBFile_to_molsysmt_Structures
    tmp_item = openmm_PDBFile_to_molsysmt_Structures(item, atom_indices=atom_indices, 
                                                     structure_indices=structure_indices, skip_digestion=True)

    if opened_here:
        item.close()

    return tmp_item
