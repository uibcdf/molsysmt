from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
import numpy as np
from molsysmt import puw

def get_ramachandran_angles(molecular_system, selection='all', structure_indices='all',
        syntaxis='MolSysMT', pbc=False, check=False):

    if check:

        digest_single_molecular_system(molecular_system)
        syntaxis = digest_syntaxis(syntaxis)
        selection = digest_selection(selection, syntaxis)
        center_of_selection = digest_selection(center_of_selection, syntaxis)
        structure_indices = digest_structure_indices(structure_indices)

    from . import get_dihedral_angles
    from molsysmt.topology import get_covalent_dihedral_quartets

    phi_covalent_chain = get_covalent_dihedral_quartets(molecular_system, dihedral_angle='phi', selection=selection, syntaxis=syntaxis, check=False)
    psi_covalent_chain = get_covalent_dihedral_quartets(molecular_system, dihedral_angle='psi', selection=selection, syntaxis=syntaxis, check=False)

    n_chains = phi_covalent_chain.shape[0]

    angles = get_dihedral_angles(molecular_system, quartets=np.vstack([phi_covalent_chain,
        psi_covalent_chain]), structure_indices=structure_indices, pbc=pbc, check=False)

    return phi_covalent_chain, psi_covalent_chain, angles[:,:n_chains], angles[:,n_chains:]

