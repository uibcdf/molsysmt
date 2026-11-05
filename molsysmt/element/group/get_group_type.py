from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.argdigest.name_resolution import DIGEST_OPTIONS


@arg_digest()
def get_group_type(
    molecular_system,
    element="group",
    selection="all",
    redefine_types=False,
    syntax="MolSysMT",
    skip_digestion=False,
):
    """
    Getting group types from a molecular system.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='group'
        Structural element level to query ('atom', 'group', 'component', 'molecule', 'chain', 'entity').
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    redefine_types : bool, default=False
        Infer types from local names, per-group naming declarations and admitted
        atom-name evidence instead of returning stored types. The input is unchanged.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of str
        List of group types ('amino acid', 'water', 'ion', 'small molecule', 'lipid', etc.).

    Notes
    -----
    Native inference uses the same bounded naming profiles as scalar recognition.
    Unknown or undeclared ambiguous labels stay unknown; a naming convention is
    never inferred from the input form. Groups with the same label but different
    declarations are interpreted independently. Querying does not rewrite stored
    names/types, chemical states or stable molecule membership. Explicit type
    reconstruction belongs to Topology.rebuild_groups.

    .. admonition:: User guide

       See :ref:`user-foundations-group-naming-schemes` and
       :ref:`Tutorial_Get_group_type` for query and reconstruction semantics.


    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    if isinstance(selection, str) and selection == "all":
        from molsysmt.native import MolSys, Topology
        from molsysmt.native._topology_infer import project_group_type_from_topology

        if isinstance(molecular_system, Topology):
            return project_group_type_from_topology(
                molecular_system, element=element, redefine_types=redefine_types
            )
        if isinstance(molecular_system, MolSys):
            return project_group_type_from_topology(
                molecular_system.topology,
                element=element,
                redefine_types=redefine_types,
            )

    if redefine_types:
        from molsysmt.basic import convert, select
        from molsysmt.native import MolSys, Topology
        from molsysmt.native._topology_infer import infer_group_types_from_topology

        topology = (
            molecular_system
            if isinstance(molecular_system, Topology)
            else molecular_system.topology
            if isinstance(molecular_system, MolSys)
            else convert(molecular_system, to_form="molsysmt.Topology")
        )
        indices = select(
            molecular_system, element=element, selection=selection, syntax=syntax
        )
        group_types = infer_group_types_from_topology(topology)
        if element == "group":
            output = group_types[indices].tolist()
        elif element == "atom":
            positions = topology.atoms.iloc[indices]["group_index"].to_numpy(
                dtype=int, na_value=-1
            )
            output = [
                group_types[index] if index >= 0 else "unknown" for index in positions
            ]
        else:
            raise NotImplementedError

    else:
        output = get(
            molecular_system,
            element=element,
            selection=selection,
            syntax=syntax,
            group_type=True,
        )

    return output


@signal(tags=["api", "element", "naming"])
@arg_digest(**DIGEST_OPTIONS)
def get_group_type_from_group_name(
    group_name, skip_digestion=False, *, naming_scheme=None
):
    """Determining a group's type under a source naming convention.

    Parameters
    ----------
    group_name : str or none
        Case-sensitive uppercase group label. Missing names remain unknown.
    skip_digestion : bool, default=False
        Skip argument digestion only for already validated inputs.
    naming_scheme : str or none, default=None
        Source vocabulary for peptide-name interpretation: 'sequence', 'amber',
        'ccd' or 'legacy'. None uses the assessed unambiguous subset. Independent
        existing water, ion and other non-peptide catalogs remain available.

    Returns
    -------
    str
        Recognized group type, such as 'amino acid', 'small molecule', 'water'
        or 'ion'. 'unknown' means missing or unassessed, not a chemical identity.

    Raises
    ------
    ArgumentError
        If a context-dependent label lacks naming_scheme or the label is invalid.
    ArgumentChoiceError
        If naming_scheme is unsupported.

    Notes
    -----
    Naming recognition does not establish an exact template or a chemical state.
    Native readers conservatively preserve ambiguous undeclared names as unknown;
    this explicit scalar query instead asks for the missing convention.
    Rebuilding group types respects stored per-group schemes without editing names,
    assignments or stable molecule membership. See the naming guide for coverage.

    Examples
    --------
    >>> get_group_type_from_group_name('ALA')
    'amino acid'
    >>> get_group_type_from_group_name('HID', naming_scheme='ccd')
    'small molecule'
    >>> get_group_type_from_group_name('HID', naming_scheme='amber')
    'amino acid'
    >>> get_group_type_from_group_name('HOH')
    'water'

    .. admonition:: User guide

       See :ref:`user-foundations-group-naming-schemes` and
       :ref:`Tutorial_Group_Name_Code` for conventions and examples.

    .. versionadded:: 1.0.0
    """
    from molsysmt import _ackredit
    from molsysmt._private.name_resolution import (
        assessed,
        classify_group_name,
        references,
    )

    result = assessed(
        group_name,
        naming_scheme,
        caller="molsysmt.element.group.get_group_type_from_group_name",
        require_context=True,
    )
    if result is None:
        return classify_group_name(group_name, naming_scheme)
    caller = "molsysmt.element.group.get_group_type_from_group_name"
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(
            provider,
            references(result.profile, alphabet=False),
            caller,
            contextual=True,
        )
    return result.group_type
