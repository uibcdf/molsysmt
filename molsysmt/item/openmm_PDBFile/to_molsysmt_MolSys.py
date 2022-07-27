from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_molsysmt_MolSys(item, selection='all', structure_indices='all', syntax='MolSysMT'):

    if check:

        digest_item(item, 'openmm.PDBFile')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from molsysmt.native.molsys import MolSys
    from .to_molsysmt_Topology import to_molsysmt_Topology
    from .to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices,
            structure_indices=structure_indices)
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices,
            structure_indices=structure_indices)

    return tmp_item

