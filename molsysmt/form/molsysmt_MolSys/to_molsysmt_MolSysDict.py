from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.MolSys")
def to_molsysmt_MolSysDict(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting from molsysmt.MolSys to molsysmt.MolSysDict.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSysDict
        Resulting object in molsysmt.MolSysDict form.

    Raises
    ------
    ValueError
        If nonempty MolecularMechanics or untyped extensions cannot be preserved
        by the declared schema. Independently absent domains are supported.

    Notes
    -----
    The writer emits schema 0.2 with explicitly optional topology, chemical states,
    structures, state associations and named analyses. Numeric arrays use typed
    transport; dimensionful fields use PyUnitWizard quantity records. Nullable
    assignments and producer history retain their stored meaning. JSON/YAML
    encoding materializes this transport; use H5MSM 0.5 for large numeric data.
    Legacy 0.1 reading remains available through the separate dictionary reader.

    Examples
    --------
    >>> import json
    >>> import molsysmt as msm
    >>> from molsysmt.native import MolSys
    >>> molsys = MolSys(n_atoms=1)
    >>> molsys.topology.atoms.loc[0, "isotope"] = 13
    >>> records = msm.convert(molsys, to_form="molsysmt.MolSysDict").to_dict()
    >>> json.loads(json.dumps(records))["topology"]["atoms"][0]["isotope"]
    13

    .. versionadded:: 1.0.0
    """

    from molsysmt.form._native_dict import encode_molsys

    source = item.extract(
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        copy_if_all=False,
        skip_digestion=True,
    )
    return encode_molsys(source)
