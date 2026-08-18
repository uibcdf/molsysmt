from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:prmtop')
def to_file_pdb(item, atom_indices='all', coordinates=None, output_filename=None, skip_digestion=False):
    """
    Converting from file:prmtop to file:pdb.

    Parameters
    ----------
    item : file:prmtop
        Source item in file:prmtop form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : numpy.ndarray or quantity
        Cartesian coordinate array in nanometers.
    output_filename : str or pathlib.Path
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:pdb
        Resulting object in file:pdb form.

    .. versionadded:: 1.0.0
    """

    from .to_openmm_Topology import to_openmm_Topology
    from molsysmt.form.openmm_Topology.to_file_pdb import to_file_pdb as openmm_Topology_to_file_pdb

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = openmm_Topology_to_file_pdb(tmp_item, coordinates=coordinates, output_filename=output_filename,
                                           skip_digestion=True)

    return tmp_item

