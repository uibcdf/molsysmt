from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.Topology')
def to_file_psf(item, atom_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from molsysmt.Topology to file:psf.

    Parameters
    ----------
    item : molsysmt.Topology
        Source item in molsysmt.Topology form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    output_filename : str or pathlib.Path
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:psf
        Resulting object in file:psf form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology
    from molsysmt.form.openmm_Topology.to_file_psf import to_file_psf as openmm_Topology_to_file_psf

    tmp_item = molsysmt_Topology_to_openmm_Topology(item, atom_indices=atom_indices)
    tmp_item = openmm_Topology_to_file_psf(tmp_item, output_filename=output_filename)

    return tmp_item

