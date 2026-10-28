from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:amino_acids_3")
def to_molsysmt_MolSys(
    item, group_indices="all", skip_digestion=False, *, structure_indices="all"
):
    """Converting sequence groups to a native system without coordinates or atoms.

    Parameters
    ----------
    item : str
        Sequence in string:amino_acids_3 form, with an optional explicit prefix.
        The corresponding topology converter defines group-code interpretation.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Original group positions in requested order; repetitions are retained.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    structure_indices : str, default='all'
        Only 'all' is accepted; no coordinate structures are present.

    Returns
    -------
    molsysmt.MolSys
        Independent partial system holding declared groups and hierarchy slots.
        No stored atom, bond or coordinate rows are synthesized. Atom-free
        hierarchy query/extraction limits remain tracked by MolSysMT #518.

    Raises
    ------
    ArgumentError
        If sequence codes or source group positions are invalid.
    NotWithThisFormError
        If coordinate structures are requested.

    See Also
    --------
    molsysmt.form.string_amino_acids_3.to_molsysmt_Topology.to_molsysmt_Topology
        Converting to the same group-level topology without a system container.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert('amino_acids_3:AlaGly', to_form='molsysmt.MolSys')
    >>> molsys.topology.n_atoms, molsys.topology.n_groups, molsys.structures.n_structures
    (0, 2, 0)

    .. admonition:: User guide

       See :ref:`Tutorial_Form_string_amino_acids_3` for the partial representation.

    .. versionadded:: 1.0.0
    """
    from molsysmt.native import MolSys

    from .to_molsysmt_Topology import to_molsysmt_Topology

    topology = to_molsysmt_Topology(
        item, group_indices=group_indices, structure_indices=structure_indices
    )
    output = MolSys()
    output.topology = topology
    return output
