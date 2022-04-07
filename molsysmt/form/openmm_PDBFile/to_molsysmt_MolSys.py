from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_openmm_PDBFile import is_openmm_PDBFile

def to_molsysmt_MolSys(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    if check:

        try:
            is_openmm_PDBFile(item)
        except:
            raise WrongFormError('openmm.PDBFile')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt.native.molsys import MolSys
    from .to_molsysmt_Topology import to_molsysmt_Topology
    from .to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item

