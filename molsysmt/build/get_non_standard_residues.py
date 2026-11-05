from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError


@arg_digest()
def get_non_standard_residues(
    molecular_system, selection="all", syntax="MolSysMT", engine="MolSysMT"
):
    """
    Reporting reference amino-acid names for non-standard groups.

    This function detects residues whose names are not part of the standard set
    recognised by the backend and maps their group indices to the names of the
    reference amino acids. A reporting parent does not authorize replacing a
    modified group or selecting its parent's chemical template.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    engine : object, default='MolSysMT'
        Argument engine.

    Returns
    -------
    dict
        Dictionary mapping group (residue) indices (int) in the original molecular
        system to reference amino-acid names (str). This is not a chemical
        replacement operation.


    Raises
    ------
    NotImplementedMethodError
        Raised if the requested ``engine`` is not supported.


    Notes
    -----
    PDBFixer delegation refuses the reviewed context-dependent labels until a
    source-naming adapter is available, including explicit declarations. Only the
    selected groups are checked. Native reference reporting remains available.

    The MolSysMT backend uses the shared naming resolver and stored per-group
    conventions in native objects, native dictionaries and H5MSM 0.5. Other
    forms have no implicit source convention. Ambiguous names without context
    require a declaration, not a guessed Amber or legacy interpretation.
    Unassessed default names and unknown parents are omitted. The PDBFixer
    backend retains its own catalogue and may report different substitutions.


    .. admonition:: User guide

       See :ref:`user-foundations-group-naming-schemes` for naming context,
       exact references and unsupported cases.

    .. versionadded:: 1.0.0
    """

    output = {}

    if engine == "MolSysMT":
        from molsysmt._private.name_resolution import stored_topology
        from molsysmt.basic import get, select
        from molsysmt.element.group.amino_acid import get_standard_name

        group_indices = select(
            molecular_system, element="group", selection=selection, syntax=syntax
        )
        topology = stored_topology(
            molecular_system, caller="molsysmt.build.get_non_standard_residues"
        )
        group_name_list = (
            topology.groups.iloc[group_indices]["group_name"].tolist()
            if topology is not None
            else get(
                molecular_system,
                element="group",
                selection=group_indices,
                group_name=True,
            )
        )
        schemes = None if topology is None else topology.group_naming_schemes
        for group_idx, group_name in zip(group_indices, group_name_list):
            standard = get_standard_name(
                group_name,
                naming_scheme=None if schemes is None else schemes[int(group_idx)],
            )
            if standard is not None:
                output[int(group_idx)] = standard

    elif engine == "PDBFixer":
        from molsysmt._private.amino_acid_templates import check_external_preparation

        check_external_preparation(
            molecular_system,
            engine,
            "molsysmt.build.get_non_standard_residues",
            selection=selection,
            syntax=syntax,
        )
        from molsysmt.basic import convert, select

        group_indices_in_selection = select(
            molecular_system, element="group", selection=selection
        )

        tmp_item = convert(
            molecular_system,
            to_form="pdbfixer.PDBFixer",
            selection=selection,
            syntax=syntax,
        )

        tmp_item.findNonstandardResidues()

        for group, substitution in tmp_item.nonstandardResidues:
            original_group_index = group_indices_in_selection[group.index]
            output[original_group_index] = (
                substitution if isinstance(substitution, str) else substitution.name
            )

    else:
        raise NotImplementedMethodError

    return output
