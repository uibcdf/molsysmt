from molsysmt._private.digestion import digest

@digest(form='mdtraj.Topology')
def to_file_top(item, atom_indices='all', output_filename=None, digest=True):

    from . import to_parmed_GromacsTopologyFile
    from ..parmed_GromacsTopologyFile import to_file_top as parmed_GromacsTopologyFile_to_file_top

    tmp_item = to_parmed_GromacsTopologyFile(item, atom_indices=atom_indices, digest=False)
    tmp_item = parmed_GromacsTopologyFile_to_file_top(tmp_item, output_filename=output_filename, digest=False)

    return tmp_item

