from depdigest import dep_digest
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='pdbfixer.PDBFixer')
@dep_digest('MDTraj')
def to_mdtraj_Trajectory(item, atom_indices='all', skip_digestion=False):

    from mdtraj.core.trajectory import Trajectory as mdtraj_Trajectory

    from molsysmt import pyunitwizard as puw
    from . import to_mdtraj_Topology
    from . import get_coordinates_from_atom

    tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    coordinates = get_coordinates_from_atom(tmp_item, indices=atom_indices, skip_digestion=True)
    coordinates = puw.convert(coordinates, to_units='nanometer', to_form='openmm.unit')
    tmp_item = mdtraj_Trajectory(coordinates, tmp_item, skip_digestion=True)

    return tmp_item

