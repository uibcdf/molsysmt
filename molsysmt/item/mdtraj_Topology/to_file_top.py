from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_file_top(item, atom_indices='all', output_filename=None, check=True):

    if check:

        digest_item(item, 'mdtraj.Topology')
        atom_indices = digest_atom_indices(atom_indices)

    from . import to_parmed_GromacsTopologyFile
    from ..parmed_GromacsTopologyFile import to_file_top as parmed_GromacsTopologyFile_to_file_top

    tmp_item = to_parmed_GromacsTopologyFile(item, atom_indices=atom_indices, check=False)
    tmp_item = parmed_GromacsTopologyFile_to_file_top(tmp_item, output_filename=output_filename, check=False)

    return tmp_item

