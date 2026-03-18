from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='mdtraj.PDBTrajectoryFile')
@dep_digest('mdtraj')
def to_mdtraj_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    return item.topology
