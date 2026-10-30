from molsysmt._private.argdigest import arg_digest
from molsysmt.native._chemical_queries import project as _project
from molsysmt.native._chemical_queries import system as _system

form = "molsysmt.ChemicalStates"


@arg_digest(form="molsysmt.ChemicalStates")
def get_n_atoms_from_system(item, skip_digestion=False):
    """Getting the atom-domain size from chemical states."""

    return item.n_atoms


@arg_digest(form="molsysmt.ChemicalStates")
def get_n_chemical_states_from_system(item, skip_digestion=False):
    """Getting the number of chemical states."""

    return item.n_chemical_states


@arg_digest(form="molsysmt.ChemicalStates")
def get_reference_chemical_state_index_from_system(item, skip_digestion=False):
    """Getting the reference chemical-state index."""

    return item.reference_chemical_state_index


@arg_digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):
    """Counting stored edges in the selected chemical state.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    int
        Stored edge count; zero does not certify complete connectivity.

    .. versionadded:: 1.0.0
    """
    return _system(item, "n_bonds")


@arg_digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):
    """Counting component rows in the selected chemical state.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection supplying state-local component inventory.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    int
        Stored component count, including declared components without atoms.

    .. versionadded:: 1.0.0
    """
    return _system(item, "n_components")


@arg_digest(form=form)
def get_chemical_state_index_from_system(item, skip_digestion=False):
    """Listing every chemical-state position without changing the reference.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Ordered collection whose complete inventory is requested.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int
        All state indices, even when another attribute selects one state.

    .. versionadded:: 1.0.0
    """
    return _system(item, "chemical_state_index")


@arg_digest(form=form)
def get_chemical_state_id_from_system(item, skip_digestion=False):
    """Listing stored string labels for the complete chemical-state inventory.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Ordered collection whose labels are requested.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        One label per state, retaining missing labels and collection order.

    .. versionadded:: 1.0.0
    """
    return _system(item, "chemical_state_id")


@arg_digest(form=form)
def get_connectivity_completeness_from_system(item, skip_digestion=False):
    """Reading the selected state's connectivity declaration without inference.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with a resolvable chemical state.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    str
        'unavailable', 'partial' or 'complete' for that state, not all states.

    .. versionadded:: 1.0.0
    """
    return _system(item, "connectivity_completeness")


@arg_digest(form=form)
def get_component_completeness_from_system(item, skip_digestion=False):
    """Reading the selected state's component-completeness declaration.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with a resolvable chemical state.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    str
        'unavailable', 'partial' or 'complete', independently of connectivity.

    .. versionadded:: 1.0.0
    """
    return _system(item, "component_completeness")


@arg_digest(form=form)
def get_component_evidence_from_system(item, skip_digestion=False):
    """Reading the selected state's recorded component evidence.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection retaining the original component assignment evidence.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    str
        Stored evidence label, without classifying or rebuilding components.

    .. versionadded:: 1.0.0
    """
    return _system(item, "component_evidence")


@arg_digest(form=form)
def get_atom_index_from_atom(item, indices="all", skip_digestion=False):
    """Returning positions on the collection's shared atom domain.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection declaring the atom-axis size, including a zero-state collection.
    indices : str or list of int, default='all'
        Atom positions, preserving requested order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        Selected atom positions; no stable names or groups are synthesized.

    .. versionadded:: 1.0.0
    """
    return _project(item, "atom", "atom_index", indices)


@arg_digest(form=form)
def get_n_atoms_from_atom(item, indices="all", skip_digestion=False):
    """Counting positions in an atom selection without requiring a state.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection declaring the shared atom-domain size.
    indices : str or list of int, default='all'
        Atom positions; repetitions contribute to the selected length.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    int or None
        Selection length, or the complete atom-domain size for 'all'.

    .. versionadded:: 1.0.0
    """
    return _project(item, "atom", "n_atoms", indices)


@arg_digest(form=form)
def get_bond_index_from_bond(item, indices="all", skip_digestion=False):
    """Returning validated positions in the selected state's bond table.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection supplying the active chemical-state axis.
    indices : str or list of int, default='all'
        Bond positions in that state, not bond IDs or another state's positions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        Ordered selected positions, including repetitions or an empty list.

    .. versionadded:: 1.0.0
    """
    return _project(item, "bond", "bond_index", indices)


@arg_digest(form=form)
def get_bond_index_from_system(item, skip_digestion=False):
    """Listing all stored bond positions in the selected chemical state.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int
        Contiguous state-local positions; an edge-free table returns [].

    .. versionadded:: 1.0.0
    """
    return _project(item, "bond", "bond_index")


@arg_digest(form=form)
def get_component_index_from_component(item, indices="all", skip_digestion=False):
    """Returning validated positions in the selected component inventory.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection supplying the active state's component rows.
    indices : str or list of int, default='all'
        Component positions, preserving order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        State-local positions, independent of Topology's stable molecules.

    .. versionadded:: 1.0.0
    """
    return _project(item, "component", "component_index", indices)


@arg_digest(form=form)
def get_component_index_from_atom(item, indices="all", skip_digestion=False):
    """Projecting stored component membership onto selected atom positions.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection supplying the selected state's atom-aligned declarations.
    indices : str or list of int, default='all'
        Atom positions, preserving order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        One component index or missing value per atom; no graph inference runs.

    .. versionadded:: 1.0.0
    """
    return _project(item, "atom", "component_index", indices)


@arg_digest(form=form)
def get_n_components_from_atom(item, indices="all", skip_digestion=False):
    """Counting distinct declared components represented by selected atoms.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection supplying state-local membership and component inventory.
    indices : str or list of int, default='all'
        Atom positions. 'all' counts the full declared component inventory.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    int or None
        Distinct known memberships for an explicit selection; missing links do
        not create components. A count does not certify completeness.

    .. versionadded:: 1.0.0
    """
    return _project(item, "atom", "n_components", indices)


@arg_digest(form=form)
def get_n_components_from_component(item, indices="all", skip_digestion=False):
    """Counting selected component positions without rebuilding their graph.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection supplying the active component inventory.
    indices : str or list of int, default='all'
        Component positions; repeated positions retain their multiplicity.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    int or None
        Selected length, including zero for an empty selection.

    .. versionadded:: 1.0.0
    """
    return _project(item, "component", "n_components", indices)


@arg_digest(form=form)
def get_n_bonds_from_atom(item, indices="all", skip_digestion=False):
    """Counting stored incident edges separately for each selected atom.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection supplying the active state's stored edges.
    indices : str or list of int, default='all'
        Atom positions, including repetitions and atoms without bonds.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        One incident-edge count per atom, including edges to unselected atoms.

    .. versionadded:: 1.0.0
    """
    return _project(item, "atom", "n_bonds", indices)


@arg_digest(form=form)
def get_bond_index_from_atom(item, indices="all", skip_digestion=False):
    """Listing stored incident bond positions for each selected atom.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection supplying the active state's stored edges.
    indices : str or list of int, default='all'
        Atom positions; external endpoints are retained in incident lists.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of list of int or None
        One ordered state-local bond list per atom; isolated atoms give [].

    .. versionadded:: 1.0.0
    """
    return _project(item, "atom", "bond_index", indices)


@arg_digest(form=form)
def get_n_atoms_from_component(item, indices="all", skip_digestion=False):
    """Counting atoms with declared membership in each selected component.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection supplying atom-aligned membership in the active state.
    indices : str or list of int, default='all'
        Component positions, including empty declared components.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        Atom count per component; atoms with unknown membership are excluded.

    .. versionadded:: 1.0.0
    """
    return _project(item, "component", "n_atoms", indices)


@arg_digest(form=form)
def get_atom_index_from_component(item, indices="all", skip_digestion=False):
    """Listing declared atom members of each selected component.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection supplying atom-aligned membership in the active state.
    indices : str or list of int, default='all'
        Component positions, preserving repeated and empty components.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of list of int or None
        Ascending source atom positions per component, without topology context.

    .. versionadded:: 1.0.0
    """
    return _project(item, "component", "atom_index", indices)


@arg_digest(form=form)
def get_n_bonds_from_component(item, indices="all", skip_digestion=False):
    """Counting distinct stored edges incident on each selected component.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection supplying stored edges and declared component memberships.
    indices : str or list of int, default='all'
        Component positions. An internal edge contributes once, not twice.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        Incident counts, including cross-component edges at both known ends.

    .. versionadded:: 1.0.0
    """
    return _project(item, "component", "n_bonds", indices)


@arg_digest(form=form)
def get_bonded_atom_pairs_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored bond participants from the selected chemical state.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Declared chemical-state provider; no stable hierarchy is required.
    indices : str or list of int, default='all'
        Ordered source positions. Atom selections restrict incident edges or,
        for inner relationships, edges with both endpoints selected.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list
        Source atom-index pairs, or sorted unique atoms for bonded_atoms.
        Empty stored connectivity returns an empty list without inference.

    .. versionadded:: 1.0.0
    """
    from molsysmt.native._chemical_relations import relation

    return relation(item, "bond", "bonded_atom_pairs", indices)


@arg_digest(form=form)
def get_bonded_atoms_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored bond participants from the selected chemical state.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Declared chemical-state provider; no stable hierarchy is required.
    indices : str or list of int, default='all'
        Ordered source positions. Atom selections restrict incident edges or,
        for inner relationships, edges with both endpoints selected.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list
        Source atom-index pairs, or sorted unique atoms for bonded_atoms.
        Empty stored connectivity returns an empty list without inference.

    .. versionadded:: 1.0.0
    """
    from molsysmt.native._chemical_relations import relation

    return relation(item, "bond", "bonded_atoms", indices)


@arg_digest(form=form)
def get_bonded_atom_pairs_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored bond participants from the selected chemical state.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Declared chemical-state provider; no stable hierarchy is required.
    indices : str or list of int, default='all'
        Ordered source positions. Atom selections restrict incident edges or,
        for inner relationships, edges with both endpoints selected.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list
        Source atom-index pairs, or sorted unique atoms for bonded_atoms.
        Empty stored connectivity returns an empty list without inference.

    .. versionadded:: 1.0.0
    """
    from molsysmt.native._chemical_relations import relation

    return relation(item, "atom", "bonded_atom_pairs", indices)


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored bond participants from the selected chemical state.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Declared chemical-state provider; no stable hierarchy is required.
    indices : str or list of int, default='all'
        Ordered source positions. Atom selections restrict incident edges or,
        for inner relationships, edges with both endpoints selected.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list
        Source atom-index pairs, or sorted unique atoms for bonded_atoms.
        Empty stored connectivity returns an empty list without inference.

    .. versionadded:: 1.0.0
    """
    from molsysmt.native._chemical_relations import relation

    return relation(item, "atom", "inner_bonded_atom_pairs", indices)


@arg_digest(form=form)
def get_bonded_atom_pairs_from_system(item, skip_digestion=False):
    """Reading stored bond participants from the selected chemical state.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Declared chemical-state provider; no stable hierarchy is required.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list
        Source atom-index pairs, or sorted unique atoms for bonded_atoms.
        Empty stored connectivity returns an empty list without inference.

    .. versionadded:: 1.0.0
    """
    from molsysmt.native._chemical_relations import relation

    return relation(item, "system", "bonded_atom_pairs", "all")


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_system(item, skip_digestion=False):
    """Reading stored bond participants from the selected chemical state.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Declared chemical-state provider; no stable hierarchy is required.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list
        Source atom-index pairs, or sorted unique atoms for bonded_atoms.
        Empty stored connectivity returns an empty list without inference.

    .. versionadded:: 1.0.0
    """
    from molsysmt.native._chemical_relations import relation

    return relation(item, "system", "inner_bonded_atom_pairs", "all")


__all__ = [name for name in globals() if name.startswith("get_")]
