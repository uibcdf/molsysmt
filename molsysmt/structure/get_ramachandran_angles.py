import numpy as np
from molsysmt import puw
from molsysmt._private_tools.structure_indices import digest_structure_indices

def get_ramachandran_angles(molecular_system, selection='all', structure_indices='all', syntaxis='MolSysMT', pbc=False):

    from molsysmt.structure import get_dihedral_angles
    from molsysmt.topology import get_covalent_dihedral_quartets
    from molsysmt.basic import is_a_molecular_system

    if not is_a_molecular_system(molecular_system):
        raise SingleMolecularSystemNeededError()

    structure_indices = digest_structure_indices(structure_indices)

    phi_covalent_chain = get_covalent_dihedral_quartets(molecular_system, dihedral_angle='phi', selection=selection, syntaxis=syntaxis)
    psi_covalent_chain = get_covalent_dihedral_quartets(molecular_system, dihedral_angle='psi', selection=selection, syntaxis=syntaxis)

    n_chains = phi_covalent_chain.shape[0]

    angles = get_dihedral_angles(molecular_system, quartets=np.vstack([phi_covalent_chain, psi_covalent_chain]), structure_indices=structure_indices, pbc=pbc)

    return phi_covalent_chain, psi_covalent_chain, angles[:,:n_chains], angles[:,n_chains:]

