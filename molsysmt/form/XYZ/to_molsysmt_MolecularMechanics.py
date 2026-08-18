from molsysmt._private.argdigest import arg_digest

@arg_digest(form='XYZ')
def to_molsysmt_MolecularMechanics(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from XYZ to molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : XYZ
        Source item in XYZ form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolecularMechanics
        Resulting object in molsysmt.MolecularMechanics form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.native.molecular_mechanics import MolecularMechanics

    tmp_item = MolecularMechanics()

    return tmp_item


