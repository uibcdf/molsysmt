from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.StructuresDict')
def to_molsysmt_MolecularMechanics(
    item,
    atom_indices='all',
    structure_indices='all',
    skip_digestion=False,
):
    """
    Converting from molsysmt.StructuresDict to molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.StructuresDict
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolecularMechanics
        Converted molecular system representation.
    """

    from molsysmt.native.molecular_mechanics import MolecularMechanics

    tmp_item = MolecularMechanics()

    return tmp_item
