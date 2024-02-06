from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def to_file_h5msm(item, atom_indices='all', structure_indices='all', output_filename=None,
        compression='gzip', compression_opts=4, int_precision='single', float_precision='single',
                  skip_digestion=False):

    from molsysmt.native import H5MSMFileHandler
    from ..molsysmt_Topology.to_file_h5msm import _add_topology_to_h5msm
    from ..molsysmt_Structures.to_file_h5msm import _add_structures_to_h5msm

    handler = H5MSMFileHandler(output_filename, io_mode='w', compression=compression,
            compression_opts=compression_opts, int_precision=int_precision,
            float_precision=float_precision, closed=False, skip_digestion=True)

    _add_topology_to_h5msm(item.topology, handler, atom_indices=atom_indices, skip_digestion=True)
    _add_structures_to_h5msm(item.structures, handler, atom_indices=atom_indices, structure_indices=structure_indices,
                            skip_digestion=True)

    handler.close()

    return output_filename

