from molsysmt._private.digestion import digest

@digest(form='mdtraj.Topology')
def to_file_top(item, atom_indices='all', output_filename=None):

    from . import to_parmed_GromacsTopologyFile
    from ..parmed_GromacsTopologyFile import to_file_top as parmed_GromacsTopologyFile_to_file_top

    tmp_item = to_parmed_GromacsTopologyFile(item, atom_indices=atom_indices)
    tmp_item = parmed_GromacsTopologyFile_to_file_top(tmp_item, output_filename=output_filename)

    return tmp_item

