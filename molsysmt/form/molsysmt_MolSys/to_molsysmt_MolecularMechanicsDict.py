from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_molsysmt_MolecularMechanicsDict(item, atom_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolecularMechanicsDict
        Converted molecular system representation.
    """

    from molsysmt.form.molsysmt_MolecularMechanics.to_molsysmt_MolecularMechanicsDict import to_molsysmt_MolecularMechanicsDict as molsysmt_MolecularMechanics_to_MolecularMechanicsDict

    tmp_item = molsysmt_MolecularMechanics_to_MolecularMechanicsDict(item.molecular_mechanics,
                                                                     atom_indices=atom_indices, skip_digestion=True)

    return tmp_item


