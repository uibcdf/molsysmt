from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_openmm_PDBFile import is_openmm_PDBFile

def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', check=True):

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

    from .to_mdtraj_Topology import to_mdtraj_Topology
    from .get import get_coordinates_from_atom

    try:
        from mdtraj.core.trajectory import Trajectory as mdtraj_Trajectory
    except:
        raise LibraryNotFoundError()

    topology = to_mdtraj_Topology(item, atom_indices=atom_indices)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item = mdtraj_Trajectory(positions, topology)

    return tmp_item

