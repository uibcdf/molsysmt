from molsysmt._private.digestion import digest_item, digest_atom_indices

def to_openmm_Topology(item, atom_indices='all', check=True):

    if check:

        digest_item(item, 'openmm.GromacsGroFile')
        atom_indices = digest_atom_indices(atom_indices)

    tmp_item = item.topology

    return tmp_item

