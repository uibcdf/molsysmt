from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:amino_acids_3")
def to_molsysmt_Topology(
    item, group_indices="all", skip_digestion=False, *, structure_indices="all"
):
    """Converting three-letter groups to a topology without representative atoms.

    Parameters
    ----------
    item : str
        Complete three-letter group codes, optionally prefixed with
        ``amino_acids_3:``. Caps and declared group order are retained directly;
        conversion does not pass through one-letter text. Unknown alphabetic
        names retain their group labels without assigning complete chemistry.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Original group positions in requested order; repetitions are retained.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    structure_indices : str, default='all'
        Only 'all' is accepted because the source contains no structures.

    Returns
    -------
    molsysmt.Topology
        Independent declared groups and one molecule/entity/chain slot, with
        zero stored atoms and bonds. Group types use known native codes;
        atomic inventory, connectivity and coordinates remain unspecified.

    Raises
    ------
    ArgumentError
        If a token is incomplete, nonalphabetic, or a source position is invalid.
    NotWithThisFormError
        If coordinate structures are requested.

    Notes
    -----
    Atom-free hierarchy limitations remain under MolSysMT #518. Group/chain
    projections, text selections, builder/dictionary reconstruction and
    atom-driven extraction require follow-up. Stored counts are representation
    counts; they do not certify physical atom composition or molecular identity.
    No Biopython dependency or atomic/coordinate construction is introduced.

    Examples
    --------
    >>> import molsysmt as msm
    >>> topology = msm.convert('amino_acids_3:AceAlaNme', to_form='molsysmt.Topology')
    >>> topology.n_atoms, topology.groups.group_name.tolist()
    (0, ['ACE', 'ALA', 'NME'])

    .. admonition:: User guide

       See :ref:`Tutorial_Form_string_amino_acids_3` for supported conversions.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form._sequence_topology import from_string

    return from_string(item, 3, group_indices, structure_indices, caller=__name__)
