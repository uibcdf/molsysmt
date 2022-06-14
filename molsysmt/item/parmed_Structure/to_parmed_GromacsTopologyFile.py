from molsysmt._private.digestion import digest_item, digest_atom_indices

def to_parmed_GromacsTopologyFile(item, atom_indices='all', check=True):

    if check:

        digest_item(item, 'parmed.Structure')
        atom_indices = digest_atom_indices(atom_indices)

    from . import extract
    from parmed.gromacs import GromacsTopologyFile as GromacsTopologyFile

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False, check=False)
    tmp_item = GromacsTopologyFile.from_structure(tmp_item)

    return tmp_item

