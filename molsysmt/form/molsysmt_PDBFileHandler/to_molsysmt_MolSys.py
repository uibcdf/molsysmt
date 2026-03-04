import os
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.PDBFileHandler')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import MolSys
    from .to_molsysmt_Topology import to_molsysmt_Topology
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from .to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler

    if isinstance(item, (str, os.PathLike)):
        item = to_molsysmt_PDBFileHandler(str(str(item)), skip_digestion=True)
        opened_here = True
    else:
        opened_here = False

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices, 
                                                 structure_indices=structure_indices, skip_digestion=True)

    if opened_here:
        item.close()

    return tmp_item
