from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
def to_file_msmh5(item, atom_indices='all', coordinates=None, output_filename=None,
        compression='gzip', compression_opts=4, int_precision='single', float_precision='single'):

    from molsysmt.native import MSMH5FileHandler
    from .write_topology_to_msmh5 import write_topology_to_msmh5

    handler = MSMH5FileHandler(output_filename, io_mode='w', compression=compression,
            compression_opts=compression_opts, int_precision=int_precision,
            float_precision=float_precision, closed=False)

    write_topology_to_msmh5(item, handler, atom_indices=atom_indices)

    handler.close()

    return output_filename

