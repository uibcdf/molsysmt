from molsysmt._private.argdigest import arg_digest


@arg_digest(form='file:structures_yaml')
def to_molsysmt_Structures(item, skip_digestion=False):
    """
    Converting from file:structures_yaml to molsysmt.Structures.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Structures
        Resulting object in molsysmt.Structures form.


    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_StructuresDict import to_molsysmt_StructuresDict
    from molsysmt.form.molsysmt_StructuresDict.to_molsysmt_Structures import to_molsysmt_Structures as _to_structures

    tmp_item = to_molsysmt_StructuresDict(item, skip_digestion=True)
    return _to_structures(tmp_item, skip_digestion=True)
