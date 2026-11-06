"""Matching explicitly named atom inventories without inferring chemistry."""

import numpy as np
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError


@signal(tags=["api", "topology"])
@arg_digest()
def get_atom_name_correspondence(
    molecular_system,
    selection="all",
    reference_molecular_system=None,
    reference_selection=None,
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Matching unique atom names and elements across selected inventories.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form providing atom names, elements and source indices.
        Coordinates and chemical assignments are not required.
    selection : str, int, list, tuple or numpy.ndarray, default='all'
        Atom population in the query. Names must be unique within this scope.
        Repeated positional indices are refused rather than duplicated.
    reference_molecular_system : molecular system or None, default=None
        Independent reference input. None uses molecular_system.
    reference_selection : str, int, list, tuple, numpy.ndarray or None, default=None
        Reference atom population. None uses selection, including when the two
        inputs differ. Use 'all' explicitly to match against an entire template.
    syntax : str, default='MolSysMT'
        Selection syntax used for both molecular systems.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    numpy.ndarray
        Detached int64 pairs with shape (n_selected_atoms, 2). Column zero is
        the query source atom index; column one is the matching reference source
        atom index. Rows follow query selection order. Indices are positions,
        not atom IDs. Two empty selections return shape (0, 2). No units apply.

    Raises
    ------
    ArgumentError
        If positional selections contain invalid, noninteger or repeated indices.
    StructuralInconsistencyError
        If a selected name is missing/duplicated, the name sets differ, or
        matching names have incompatible elements.

    Notes
    -----
    This is an exact label correspondence, not chemical isomorphism or an
    identity guarantee. Names are case-sensitive and are not trimmed, renamed
    or guessed. Select one named component when names repeat elsewhere.
    Elements use MolSysMT atom_type semantics, independently of force-field
    types. Isotopes, bonds, charges, hydrogen policy and stereochemistry remain
    outside this operation and require separate chemical assessment.
    Neither input is changed; coordinates and chemical states are not read.

    For assess_chemical_template, pass the template as molecular_system and
    the observed system as reference_molecular_system. The resulting column
    order is then template index followed by observed source index, as that
    operation requires. Its chemistry/graph checks remain mandatory.

    See Also
    --------
    molsysmt.physchem.assess_chemical_template
        Verify explicitly mapped chemistry before applying a template.
    molsysmt.chemical_states.get_atom_correspondences
        Enumerate correspondences using complete declared chemical context.

    Examples
    --------
    >>> import molsysmt as msm
    >>> source = msm.systems['caffeine']['caffeine.sdf']
    >>> msm.topology.get_atom_name_correspondence(source, selection=[0, 2]).tolist()
    [[0, 0], [2, 2]]

    .. admonition:: User guide

       See :ref:`Tutorial_Get_Atom_Name_Correspondence` for exact label matching
       and separate chemical assessment.

    .. versionadded:: 1.0.0
    """
    reference = (
        molecular_system
        if reference_molecular_system is None
        else reference_molecular_system
    )
    reference_selection = (
        selection if reference_selection is None else reference_selection
    )
    caller = "molsysmt.topology.get_atom_name_correspondence"
    query_indices, query_names, query_types = _inventory(
        molecular_system, selection, syntax, caller, "selection"
    )
    reference_indices, reference_names, reference_types = _inventory(
        reference, reference_selection, syntax, caller, "reference_selection"
    )
    if set(query_names) != set(reference_names):
        raise StructuralInconsistencyError(
            "Selected query and reference atom-name sets differ.", caller=caller
        )
    by_name = dict(
        zip(reference_names, zip(reference_indices, reference_types), strict=True)
    )
    pairs = np.empty((len(query_indices), 2), dtype=np.int64)
    for row, (index, name, element) in enumerate(
        zip(query_indices, query_names, query_types, strict=True)
    ):
        reference_index, reference_element = by_name[name]
        if element != reference_element:
            raise StructuralInconsistencyError(
                f"Atom name {name!r} has conflicting query/reference elements.",
                caller=caller,
            )
        pairs[row] = index, reference_index
    return pairs


def _inventory(molecular_system, selection, syntax, caller, argument):
    from molsysmt.basic import get, select
    from molsysmt.element.atom import normalize_atom_types

    indices = np.asarray(
        select(molecular_system, selection=selection, element="atom", syntax=syntax),
        dtype=np.int64,
    )
    if len(np.unique(indices)) != len(indices):
        raise ArgumentError(
            argument,
            value=indices.tolist(),
            caller=caller,
            message="A name correspondence requires unique positional indices.",
        )
    names, elements = get(
        molecular_system,
        element="atom",
        selection=indices,
        atom_name=True,
        atom_type=True,
        syntax=syntax,
    )
    names = list(names)
    if len(names) != len(indices) or len(elements) != len(indices):
        raise StructuralInconsistencyError(
            "Selected atom names and elements must align with the source index axis.",
            caller=caller,
        )
    if any(not isinstance(name, str) or not name.strip() for name in names):
        raise StructuralInconsistencyError(
            "Selected atoms require explicit nonempty atom names.", caller=caller
        )
    if len(set(names)) != len(names):
        raise StructuralInconsistencyError(
            "Selected atoms have duplicate atom names; restrict the scope explicitly.",
            caller=caller,
        )
    normalized, _ = normalize_atom_types(list(elements))
    return indices, names, normalized
