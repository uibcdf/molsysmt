from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_file_h5msm(item, atom_indices='all', structure_indices='all', output_filename=None,
        compression='gzip', compression_opts=4, int_precision='single', float_precision='single',
                  skip_digestion=False):
    """
    Converting from molsysmt.MolSys to file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    compression : object, default='gzip'
        Argument compression.
    compression_opts : object, default=4
        Argument compression_opts.
    int_precision : object, default='single'
        Argument int_precision.
    float_precision : object, default='single'
        Argument float_precision.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:h5msm
        Resulting object in file:h5msm form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.native import H5MSMFileHandler
    from ..molsysmt_Topology.to_file_h5msm import dump_topology_to_h5msm
    from ..molsysmt_Structures.to_file_h5msm import dump_structures_to_h5msm

    handler = H5MSMFileHandler(output_filename, io_mode='w', compression=compression,
            compression_opts=compression_opts, int_precision=int_precision,
            float_precision=float_precision, closed=False, skip_digestion=True)

    dump_topology_to_h5msm(item.topology, handler, atom_indices=atom_indices)
    dump_structures_to_h5msm(item.structures, handler, atom_indices=atom_indices, structure_indices=structure_indices)

    n_structures = int(handler.file['structures'].attrs['n_structures_written'])
    if n_structures:
        import pandas as pd

        state_indices = item._get_structure_chemical_state_indices(
            structure_indices=structure_indices, resolved=True
        )
        encoded = [
            -1 if pd.isna(state_index) else int(state_index)
            for state_index in state_indices
        ]
        dataset = handler.file['structures']['chemical_state_index']
        dataset.resize((n_structures,))
        dataset[:] = encoded

    handler.close()

    return output_filename
