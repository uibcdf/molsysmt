from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='mdtraj.DCDTrajectoryFile')
def to_molsysmt_MolSysOld(item, atom_indices='all', structure_indices='all'):

    from molsysmt.native.topology_old import TopologyOld
    from molsysmt.native.molsys_old import MolSysOld
    from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
    from molsysmt.form.molsysmt_Structures.get import get_n_atoms_from_system

    tmp_item = MolSysOld()
    tmp_item.structures = to_molsysmt_StructuresOld(item, atom_indices=atom_indices, structure_indices=structure_indices)
    n_atoms = get_n_atoms_from_system(tmp_item.structures)
    tmp_item.topology = TopologyOld(n_atoms)

    return tmp_item

