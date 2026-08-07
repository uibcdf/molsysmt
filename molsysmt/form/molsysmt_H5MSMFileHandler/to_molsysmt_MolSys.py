import os
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.H5MSMFileHandler')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', get_missing_bonds=True,
                       skip_digestion=False):

    from molsysmt.native import MolSys
    from .to_molsysmt_Topology import to_molsysmt_Topology
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from .get_structural_attributes import (
        get_structure_chemical_state_index_from_system,
    )

    if isinstance(item, (str, os.PathLike)):
        item = to_molsysmt_H5MSMFileHandler(str(str(item)), skip_digestion=True)
        opened_here = True
    else:
        opened_here = False

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices, 
                                                 structure_indices=structure_indices, skip_digestion=True)
    state_indices = get_structure_chemical_state_index_from_system(
        item, structure_indices=structure_indices, skip_digestion=True
    )
    if state_indices:
        tmp_item._set_structure_chemical_state_indices(state_indices)

    if opened_here:
        item.close()

    return tmp_item
