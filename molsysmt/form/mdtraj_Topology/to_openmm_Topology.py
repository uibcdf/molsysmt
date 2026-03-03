from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='mdtraj.Topology')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):

    from ..openmm_Topology.extract import extract as extract_openmm_Topology
    from mdtraj.core.topology import Topology as mdtraj_Topology

    if not isinstance(item, mdtraj_Topology):
        if hasattr(item, 'topology'):
            item = item.topology
        else:
            from .to_mdtraj_Topology import to_mdtraj_Topology
            item = to_mdtraj_Topology(item, skip_digestion=True)

    tmp_item = item.to_openmm()
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item

