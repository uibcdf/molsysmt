from molsysmt._private.digestion import digest_item, digest_atom_indices

def to_openmm_Topology(item, atom_indices='all'):

    if check:

        digest_item(item, 'parmed.Structure')
        atom_indices = digest_atom_indices(atom_indices)

    from ..openmm_Topology import extract as extract_openmm_Topology

    tmp_item = tmp_item.topology
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices, copy_if_all=False,
            check=False)

    return tmp_item

