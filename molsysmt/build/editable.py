from molsysmt._private.argdigest import arg_digest


@arg_digest()
def editable(molecular_system=None, skip_digestion=False):
    """
    Creating an editable molecular-system builder.


    Parameters
    ----------
    molecular_system : molecular system, default=None
        Molecular system in any supported MolSysMT format.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSysBuilder
        Editable builder initialized either from scratch or from the input
        molecular system.
    """

    from molsysmt import MolSysBuilder
    from molsysmt.basic import convert

    if molecular_system is None:
        return MolSysBuilder(skip_digestion=True)

    return convert(molecular_system, to_form="molsysmt.MolSysBuilder", skip_digestion=True)
