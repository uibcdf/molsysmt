from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_molsysmt_MolecularMechanicsDict(item, atom_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to molsysmt.MolecularMechanicsDict.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolecularMechanicsDict
        Resulting object in molsysmt.MolecularMechanicsDict form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.molsysmt_MolecularMechanics.to_molsysmt_MolecularMechanicsDict import to_molsysmt_MolecularMechanicsDict as molsysmt_MolecularMechanics_to_MolecularMechanicsDict

    tmp_item = molsysmt_MolecularMechanics_to_MolecularMechanicsDict(item.molecular_mechanics,
                                                                     atom_indices=atom_indices, skip_digestion=True)

    return tmp_item


