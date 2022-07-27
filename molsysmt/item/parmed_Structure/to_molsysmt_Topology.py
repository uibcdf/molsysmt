from molsysmt._private.digestion import digest_item, digest_atom_indices

def to_molsysmt_Topology(item, atom_indices='all'):

    if check:

        digest_item(item, 'parmed.Structure')
        atom_indices = digest_atom_indices(atom_indices)

    from . import to_openmm_Topology
    from ..openmm_Topology import to_molsysmt_Topology

    tmp_item = to_openmm_Topology(item)
    tmp_item = openmm_Topology_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

