from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='mdtraj.DCDTrajectoryFile')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all'):

    from molsysmt.native.topology import Topology
    from molsysmt.native.molsys import MolSys
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get import get_n_atoms_from_system

    tmp_item = MolSys()
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)
    n_atoms = get_n_atoms_from_system(tmp_item.structures)
    tmp_item.topology = Topology(n_atoms)

    return tmp_item

def _to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)

