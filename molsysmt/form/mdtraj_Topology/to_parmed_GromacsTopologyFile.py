from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_parmed_GromacsTopologyFile(item, atom_indices='all', check=True):

    if check:

        digest_item(item, 'mdtraj.Topology')
        atom_indices = digest_atom_indices(atom_indices)

    from . import to_parmed_Structure
    from .parmed_Structure import to_parmed_GromacsTopologyFile as parmed_Structure_to_parmed_GromacsTopologyFile

    tmp_item = to_parmed_Structure(item, atom_indices=atom_indices, check=False)
    tmp_item = parmed_Structure_to_parmed_GromacsTopologyFile(tmp_item, check=False)

    return tmp_item

