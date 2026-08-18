from molsysmt._private.argdigest import arg_digest

@arg_digest(form='pdbfixer.PDBFixer')
def to_openmm_Modeller(item, atom_indices='all', skip_digestion=False):
    """
    Converting from pdbfixer.PDBFixer to openmm.Modeller.

    Parameters
    ----------
    item : pdbfixer.PDBFixer
        Source item in pdbfixer.PDBFixer form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Modeller
        Resulting object in openmm.Modeller form.

    .. versionadded:: 1.0.0
    """

    from molsysmt import pyunitwizard as puw
    from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    coordinates = get_coordinates_from_atom(tmp_item, indices=atom_indices, skip_digestion=True)
    coordinates = puw.convert(coordinates, to_unit='nanometer', to_form='openmm.unit')
    tmp_item = openmm_Modeller(tmp_item, coordinates)

    return tmp_item
