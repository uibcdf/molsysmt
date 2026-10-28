from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:amino_acids_1")
def to_molsysmt_Topology(
    item, group_indices="all", skip_digestion=False, *, structure_indices="all"
):
    """Converting one-letter sequence groups to a topology without atoms.

    Parameters
    ----------
    item : str
        Amino-acid sequence, optionally prefixed with ``amino_acids_1:``.
        Native ambiguous/rare codes are retained as group-level declarations.
        Gaps, stops and unsupported symbols require explicit interpretation.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Original group positions in requested order; repetitions are retained.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    structure_indices : str, default='all'
        Only 'all' is accepted because the source contains no structures.

    Returns
    -------
    molsysmt.Topology
        Independent topology with declared groups and one molecule/entity/chain
        slot. Atom and bond tables are empty; no atomic composition or geometry
        is inferred. Stored atom count zero describes represented rows, not the
        physical atom count of the declared molecule.

    Raises
    ------
    ArgumentError
        If a group code or source position is invalid.
    NotWithThisFormError
        If coordinate structures are requested.

    Notes
    -----
    Ordered chain/group membership is represented independently of atoms.
    Native hierarchy queries, text selections, extraction and dictionary/H5MSM
    round trips preserve it. Stored counts describe representation, not complete
    physical composition or chemical identity. No Biopython dependency is needed.
    Atomic construction is an explicit build operation, not an implicit CA model.

    Examples
    --------
    >>> import molsysmt as msm
    >>> topology = msm.convert('amino_acids_1:AG', to_form='molsysmt.Topology')
    >>> topology.n_atoms, topology.groups.group_name.tolist()
    (0, ['ALA', 'GLY'])

    .. admonition:: User guide

       See :ref:`Tutorial_Form_string_amino_acids_1` for supported conversions.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form._sequence_topology import from_string

    return from_string(item, 1, group_indices, structure_indices, caller=__name__)
