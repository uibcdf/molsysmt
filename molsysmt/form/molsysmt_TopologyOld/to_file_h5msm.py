from molsysmt._private.digestion import digest

@digest(form='molsysmt.TopologyOld')
def to_file_h5msm(item, atom_indices='all', coordinates=None, output_filename=None,
                  compression='gzip', compression_opts=4, int_precision='single', float_precision='single',
                  skip_digestion=False):

    from molsysmt.native import H5MSMFileHandler
    from .write_topology_to_h5msm import write_topology_to_h5msm

    handler = H5MSMFileHandler(output_filename, io_mode='w', compression=compression,
            compression_opts=compression_opts, int_precision=int_precision,
            float_precision=float_precision, closed=False, skip_digestion=True)

    write_topology_to_h5msm(item, handler, atom_indices=atom_indices)

    handler.close()

    return output_filename

