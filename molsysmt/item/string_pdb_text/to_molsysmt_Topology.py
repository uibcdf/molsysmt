from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_molsysmt_Topology(item, atom_indices='all', structure_indices='all'):

    if check:

        digest_item(item, 'string:pdb_text')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import to_molsysmt_Topology as openmm_PDBFile_to_molsysmt_Topology

    tmp_item = to_openmm_PDBFile(item)
    tmp_item = openmm_PDBFile_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

