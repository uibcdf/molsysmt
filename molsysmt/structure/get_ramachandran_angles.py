from molsysmt._private.digestion import digest
import numpy as np
from molsysmt import pyunitwizard as puw

@digest()
def get_ramachandran_angles(molecular_system, selection='all', structure_indices='all',
        syntax='MolSysMT', pbc=False):

    from . import get_dihedral_angles
    from molsysmt.topology import get_dihedral_quartets

    phi_covalent_chain = get_dihedral_quartets(molecular_system, dihedral_angle='phi', selection=selection, syntax=syntax)
    psi_covalent_chain = get_dihedral_quartets(molecular_system, dihedral_angle='psi', selection=selection, syntax=syntax)

    n_chains = phi_covalent_chain.shape[0]

    angles = get_dihedral_angles(molecular_system, quartets=np.vstack([phi_covalent_chain,
        psi_covalent_chain]), structure_indices=structure_indices, pbc=pbc)

    return phi_covalent_chain, psi_covalent_chain, angles[:,:n_chains], angles[:,n_chains:]

