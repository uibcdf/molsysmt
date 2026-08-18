from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:alphafold_id')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from string:alphafold_id to molsysmt.Structures.

    Parameters
    ----------
    item : string:alphafold_id
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Structures
        Converted molecular system representation.
    """

    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys.to_molsysmt_Structures import to_molsysmt_Structures as molsysmt_MolSys_to_molsysmt_Structures

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    tmp_item = molsysmt_MolSys_to_molsysmt_Structures(tmp_item, atom_indices=atom_indices,
                                                       structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

