from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *


def to_openmm_Topology(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'string:pdb_text')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import to_openmm_Topology as openmm_PDBFile_to_openmm_Topology

    tmp_item = to_openmm_PDBFile(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item = openmm_PDBFile_to_openmm_Topology(tmp_item, check=False)

    return tmp_item

