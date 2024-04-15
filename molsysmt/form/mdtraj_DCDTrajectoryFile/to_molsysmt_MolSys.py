from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='mdtraj.DCDTrajectoryFile')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import Topology
    from molsysmt.native import MolSys
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures import get_n_atoms_from_system

    tmp_item = MolSys()
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                 structure_indices=structure_indices, skip_digestion=True)
    n_atoms = get_n_atoms_from_system(tmp_item.structures, skip_digestion=True)
    tmp_item.topology = Topology(n_atoms=n_atoms)

    return tmp_item

