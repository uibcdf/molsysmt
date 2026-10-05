"""Applying bounded native candidates through the chemical-state authority."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "build"])
@arg_digest()
def infer_covalent_bonds(
    molecular_system,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    method="supported_group_templates",
    return_report=False,
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Inferring bounded covalent connectivity in a detached native system.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form providing atom names, elements and group membership.
        PDB input is read with inference disabled before applying this policy.
    selection : str, list, tuple or numpy.ndarray, default='all'
        Atom selection. Both candidate endpoints must be selected; full groups
        and source backbone competitors are examined before output filtering.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        One source structure for peptide geometry, or 'all' for a single structure
        or a topology without coordinates. All source structures are retained.
    chemical_state : str, int or None, default='reference'
        Destination state, or 'structure' for the chosen structure's association.
        The state must resolve unambiguously; the reference selection is preserved.
    method : str, default='supported_group_templates'
        Experimental composition of exact heavy-group templates, local observed-H
        parent consensus and unique same-chain peptide C-N distance candidates.
    return_report : bool, default=False
        Return a dictionary with molecular_system and report when True. The
        output retains historical evidence regardless of this option.
    syntax : str, default='MolSysMT'
        Syntax used for atom selection. Defaults to 'MolSysMT'.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys or dict
        Detached system, optionally accompanied by covalent_inference@1 evidence.
        Source atoms, structures, labels and declared edges are retained. Only
        missing eligible pairs are appended as inferred covalent bonds with
        unknown orders and a provenance_index into the state's preparation history.

    Raises
    ------
    ArgumentError
        If method, selection, structure or state arguments are invalid.
    StructuralInconsistencyError
        If the chemical state cannot be resolved or domain correspondence fails.
    NotWithThisFormError
        If required atom/group hierarchy is unavailable.

    Notes
    -----
    This explicitly applies local candidate evidence; it does not certify a
    complete graph, protonation, bond orders, H placement or polymer sequence.
    Unknown groups, H names and mixed H inventories remain recorded exclusions.
    No atoms are added and no distance fallback repairs arbitrary groups.
    Disulfides and metal coordination are separate policies. Peptide geometry
    uses pbc=False and the existing 0.153 nm effective ceiling.

    Added bonds make connectivity completeness partial and invalidate all named
    interaction occurrences on the output. Unchanged outputs retain their analyses.
    History keeps original operation indices after extraction or later edits;
    it is not a live assignment store. H5MSM preserves typed evidence and explicit
    quantity records without coordinate snapshots. Full native conversion/copying
    can materialize structures; this operation is not streaming.

    See Also
    --------
    get_covalent_bond_candidates : Inspect heavy or observed-H candidates.
    get_peptide_bond_candidates : Inspect bounded inter-group candidates.
    add_missing_bonds : Apply the separate legacy template/geometric policy.

    Examples
    --------
    >>> import molsysmt as msm
    >>> result = msm.build.infer_covalent_bonds(
    ...     msm.systems['T4 lysozyme L99A']['181l.pdb'], return_report=True)
    >>> result['report']['method']
    'supported_group_templates'
    >>> result['report']['n_added_bonds']
    1309

    .. admonition:: User guide

       See :ref:`Tutorial_Infer_Covalent_Bonds` for application and exclusions.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.covalent_inference import apply
    from molsysmt._private.smonitor import ArgumentError

    # Remove when the public ArgDigest floor includes uibcdf/argdigest#17.
    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(skip_digestion, caller=__name__ + ".infer_covalent_bonds")
    if method != "supported_group_templates":
        raise ArgumentError("method", value=method, caller=__name__)
    return apply(
        molecular_system,
        selection,
        structure_indices,
        chemical_state,
        return_report,
        syntax,
    )
