from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='mdtraj.Trajectory')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):

    from ..mdtraj_Topology.extract import extract as extract_mdtraj_Topology
    from mdtraj.core.topology import Topology as mdtraj_Topology

    if isinstance(item, mdtraj_Topology):
        tmp_item = item
    elif hasattr(item, 'topology'):
        tmp_item = item.topology
    else:
        # Emergency path for file handlers or strings
        import mdtraj as mdt
        if isinstance(item, str):
            tmp_item = mdt.load_topology(item)
        else:
            # Maybe a handler?
            tmp_item = item.topology

    tmp_item = extract_mdtraj_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

