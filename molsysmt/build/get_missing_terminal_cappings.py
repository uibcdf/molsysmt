from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest()
@dep_digest("pdbfixer", when={"engine": "PDBFixer"})
def get_missing_terminal_cappings(
    molecular_system,
    selection="all",
    syntax="MolSysMT",
    engine="MolSysMT",
    *,
    skip_digestion=False,
):
    """
    Identifying terminal capping atoms missing from chain termini.

    This function detects atoms expected at the C-terminus of protein chains that are
    absent from the current structure. Currently the only terminal heavy atom checked is
    ``OXT`` (C-terminal oxygen). The result maps group (residue) indices to the list of
    missing terminal atoms.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Group selection: a query string or 0-based group indices. Selection
        filters reported groups; it never creates a terminus at a selection edge.
        The native engine inspects complete chains containing selected groups.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    engine : {'MolSysMT', 'PDBFixer'}, default='MolSysMT'
        Detector of missing terminal atoms. The native rule reads stored
        backbone connectivity; PDBFixer retains its independent algorithm.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated inputs.

    Returns
    -------
    dict
        Dictionary mapping group (residue) indices (int) in the original molecular
        system to lists of missing terminal atom names (list of str). Only terminal
        groups with missing cappings are included.


    Raises
    ------
    NotImplementedError
        Raised if the requested ``engine`` is not supported.
    StructuralInconsistencyError
        If selected amino-acid groups lack known chain membership or required
        stable/chemical domains are inconsistent.


    Warns
    -----
    UnassessedPeptideBackboneWarning
        If a selected chain has incomplete, branched or unsupported backbone
        evidence. That chain contributes no endpoint; other assessed chains
        remain in the dictionary. An empty dictionary then is not a certificate
        of complete terminal chemistry.


    Notes
    -----
    The native engine reuses ``chemical_states.get_peptide_termini``: stored
    named N-CA-C motifs and inter-group C-N bonds establish the observed backbone
    direction. Atom/group positions and group IDs never define chemical order.
    Connected cycles and declared stored cap attachments have no free carboxyl
    end. Ambiguous backbones contribute no endpoints and emit a catalog warning;
    this does not certify protonation, bond order or chemical completeness.

    Selection filters the final report after full-chain terminal recognition;
    an internal selected group is not reinterpreted as a chain terminus.
    Non-amino-acid chains (water, ions, small molecules) are silently skipped.
    Unknown chain membership cannot establish a terminus. The native engine
    requires one known chain index per selected group when amino acids are
    present; it does not infer a chain from an unknown legacy sentinel.


    .. versionadded:: 1.0.0
    """

    output = {}

    if engine == "MolSysMT":
        from molsysmt.basic import get, select
        from molsysmt.chemical_states import get_peptide_termini
        from molsysmt.element.group.amino_acid import group_names as aa_names

        group_indices = select(
            molecular_system, element="group", selection=selection, syntax=syntax
        )
        group_names = get(
            molecular_system, element="group", selection=group_indices, group_name=True
        )
        if not any(name in aa_names for name in group_names):
            return output
        report = get_peptide_termini(
            molecular_system,
            selection=f"group_index in {list(group_indices)}",
            on_ambiguous="report",
        )
        from molsysmt.chemical_states._peptide_termini import warn_unassessed

        warn_unassessed(report)
        for group_index in report["c_terminal_group_indices"]:
            atom_names = get(
                molecular_system,
                selection=f"group_index=={int(group_index)}",
                atom_name=True,
            )
            if "OXT" not in atom_names:
                output[int(group_index)] = ["OXT"]

    elif engine == "PDBFixer":
        from molsysmt.basic import convert, select

        group_indices_in_selection = select(
            molecular_system, element="group", selection=selection
        )

        temp_molecular_system = convert(
            molecular_system,
            to_form="pdbfixer.PDBFixer",
            selection=selection,
            syntax=syntax,
        )

        temp_molecular_system.findMissingResidues()
        temp_molecular_system.findMissingAtoms()

        for group, atoms in temp_molecular_system.missingTerminals.items():
            original_group_index = group_indices_in_selection[group.index]
            output[original_group_index] = atoms

    else:
        raise NotImplementedError

    return output
