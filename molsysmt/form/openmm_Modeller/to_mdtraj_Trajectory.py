from .is_openmm_Modeller import is_openmm_Modeller
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private.exceptions import LibraryNotFound
from molsysmt._private.atom_indices import digest_atom_indices
from molsysmt._private.structure_indices import digest_structure_indices

def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_openmm_Modeller(item)
        except:
            raise WrongFormError('openmm.Modeller')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    try:
        from mdtraj.core.trajectory import Trajectory as mdtraj_Trajectory
    except:
        raise LibraryNotFound('MDTraj')

    from . import to_mdtraj_Topology
    from ..mdtraj_Trajectory import extract as extract_mdtraj_Trajectory
    from molsysmt import puw

    tmp_topology  = to_mdtraj_Topology(item, check=False)
    positions = puw.get_value(item.positions, to_unit='nanometers')
    tmp_item = mdtraj_Trajectory(positions, tmp_topology)
    tmp_item = extract_mdtraj_Trajectory(tmp_item, atom_indices=atom_indices,
                                         structure_indices=structure_indices, copy_if_all=False,
                                         check=False)

    return tmp_item

