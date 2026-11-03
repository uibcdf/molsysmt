from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.Topology")
def to_molsysmt_TopologyDict(item, skip_digestion=False, *, atom_indices="all"):
    """
    Converting from molsysmt.Topology to molsysmt.TopologyDict.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : str or array-like of int, default='all'
        Atom positions retained in the stable inventory projection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.TopologyDict
        Resulting object in molsysmt.TopologyDict form.


    Notes
    -----
    Schema 0.2 stores stable inventory and declared memberships, including
    group-free atom/molecule declarations. Nullable table fields become Python
    scalars or None, including typed isotope numbers. Bonds, components and
    chemical states are outside TopologyDict; use MolSysDict 0.2 or H5MSM 0.5
    for the independent chemical collection. Unsupported extension payloads reject.

    Examples
    --------
    >>> import json
    >>> import molsysmt as msm
    >>> from molsysmt.native import MolSys
    >>> molsys = MolSys(n_atoms=1)
    >>> molsys.topology.atoms.loc[0, "isotope"] = 13
    >>> records = msm.convert(molsys.topology, to_form="molsysmt.TopologyDict").to_dict()
    >>> json.loads(json.dumps(records))["atoms"][0]["isotope"]
    13

    .. versionadded:: 1.0.0
    """

    from molsysmt.form._native_dict import encode_topology

    return encode_topology(
        item.extract(atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)
    )
