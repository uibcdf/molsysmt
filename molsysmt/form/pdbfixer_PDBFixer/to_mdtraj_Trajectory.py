from .is_pdbfixer_PDBFixer import is_pdbfixer_PDBFixer
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_mdtraj_Trajectory(item, atom_indices='all', check=True):

    if check:

        try:
            is_pdbfixer_PDBFixer(item)
        except:
            raise WrongFormError('pdbfixer.PDBFixer')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    try:
        from mdtraj.core.trajectory import Trajectory as mdtraj_Trajectory
    except:
        raise LibraryNotFoundError('MDTraj')

    from molsysmt import puw
    from . import to_mdtraj_Topology
    from . import get_coordinates_from_atom

    tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices, check=False)
    coordinates = get_coordinates_from_atom(tmp_item, indices=atom_indices, check=False)
    coordinates = puw.convert(coordinates, to_units='nanometer', to_form='openmm.unit')
    tmp_item = mdtraj_Trajectory(coordinates, tmp_item)

    return tmp_item

