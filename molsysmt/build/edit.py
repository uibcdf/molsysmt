from molsysmt._private.arg_digestion import arg_digest


@arg_digest()
def edit(molecular_system, skip_digestion=False):
    """
    Creating an editable molecular-system builder from an existing molecular system.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form.

    Returns
    -------
    molsysmt.MolSysBuilder
        Editable builder initialized from the input molecular system.
    """

    from molsysmt.basic import convert

    return convert(molecular_system, to_form="molsysmt.MolSysBuilder", skip_digestion=True)
