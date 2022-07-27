from .is_pdbfixer_PDBFixer import is_pdbfixer_PDBFixer
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_mdtraj_Topology(item, atom_indices='all'):

    if check:

        try:
            is_pdbfixer_PDBFixer(item)
        except:
            raise WrongFormError('pdbfixer.PDBFixer')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    from . import to_openmm_Topology
    from ..openmm_Topology import to_mdtraj_Topology as openmm_Topology_to_mdtraj_Topology

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices)
    tmp_item = openmm_Topology_to_mdtraj_Topology(tmp_item)

    return tmp_item

