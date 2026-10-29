"""Read typed chemical columns without native-state conversion."""

from molsysmt._private.argdigest import arg_digest
from molsysmt.native._chemical_dict_queries import field as _field
from molsysmt.native._chemical_dict_queries import project as _project
from molsysmt.native._chemical_dict_queries import system as _system

form = "molsysmt.ChemicalStatesDict"


@arg_digest(form="molsysmt.ChemicalStatesDict")
def get_n_atoms_from_system(item, skip_digestion=False):
    """Getting the atom-domain size from chemical states."""

    return _system(item, "n_atoms")


@arg_digest(form="molsysmt.ChemicalStatesDict")
def get_n_chemical_states_from_system(item, skip_digestion=False):
    """Getting the number of chemical states."""

    return _system(item, "n_chemical_states")


@arg_digest(form="molsysmt.ChemicalStatesDict")
def get_reference_chemical_state_index_from_system(item, skip_digestion=False):
    """Getting the reference chemical-state index."""

    return _system(item, "reference_chemical_state_index")


@arg_digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):
    """Counting stored edges in the selected chemical state.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
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
    item : molsysmt.ChemicalStatesDict
        Typed payload supplying state-local component inventory.
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
    item : molsysmt.ChemicalStatesDict
        Ordered payload whose complete inventory is requested.
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
    item : molsysmt.ChemicalStatesDict
        Ordered payload whose labels are requested.
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
    item : molsysmt.ChemicalStatesDict
        Typed payload with a resolvable chemical state.
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
    item : molsysmt.ChemicalStatesDict
        Typed payload with a resolvable chemical state.
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
    item : molsysmt.ChemicalStatesDict
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
    item : molsysmt.ChemicalStatesDict
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
    item : molsysmt.ChemicalStatesDict
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
    item : molsysmt.ChemicalStatesDict
        Typed payload supplying the active chemical-state axis.
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
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
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
    item : molsysmt.ChemicalStatesDict
        Typed payload supplying the active state's component rows.
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
    item : molsysmt.ChemicalStatesDict
        Typed payload supplying the selected state's atom-aligned declarations.
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
    item : molsysmt.ChemicalStatesDict
        Typed payload supplying state-local membership and component inventory.
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
    item : molsysmt.ChemicalStatesDict
        Typed payload supplying the active component inventory.
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
    item : molsysmt.ChemicalStatesDict
        Typed payload supplying the active state's stored edges.
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
    item : molsysmt.ChemicalStatesDict
        Typed payload supplying the active state's stored edges.
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
    item : molsysmt.ChemicalStatesDict
        Typed payload supplying atom-aligned membership in the active state.
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
    item : molsysmt.ChemicalStatesDict
        Typed payload supplying atom-aligned membership in the active state.
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
    item : molsysmt.ChemicalStatesDict
        Typed payload supplying stored edges and declared component memberships.
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
def get_formal_charge_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored integer formal charges in elementary-charge units.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None, or None
        Formal charge per atom, in integer multiples of the elementary charge;
        not a partial charge or a summed system charge.
        An absent atom-property column returns None; a materialized column retains
        one nullable value per selected atom, including an empty list for no atoms.

    .. versionadded:: 1.0.0
    """
    return _field(item, "atom", "formal_charge", indices)


@arg_digest(form=form)
def get_atom_is_aromatic_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored atom aromaticity assignments.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of bool or None, or None
        Declared aromaticity per atom; no ring perception or aromaticity model
        is executed.
        An absent atom-property column returns None; a materialized column retains
        one nullable value per selected atom, including an empty list for no atoms.

    .. versionadded:: 1.0.0
    """
    return _field(item, "atom", "atom_is_aromatic", indices)


@arg_digest(form=form)
def get_n_unpaired_electrons_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored unpaired-electron counts.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None, or None
        Assigned unpaired-electron count per atom; unknown radical state remains
        missing.
        An absent atom-property column returns None; a materialized column retains
        one nullable value per selected atom, including an empty list for no atoms.

    .. versionadded:: 1.0.0
    """
    return _field(item, "atom", "n_unpaired_electrons", indices)


@arg_digest(form=form)
def get_n_implicit_hydrogens_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored implicit-hydrogen counts.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None, or None
        Assigned implicit-hydrogen count per atom; no valence completion is performed.
        An absent atom-property column returns None; a materialized column retains
        one nullable value per selected atom, including an empty list for no atoms.

    .. versionadded:: 1.0.0
    """
    return _field(item, "atom", "n_implicit_hydrogens", indices)


@arg_digest(form=form)
def get_n_explicit_hydrogens_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored explicit-hydrogen counts.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None, or None
        Assigned explicit-hydrogen count per atom; bonds and atom inventory are
        not recounted.
        An absent atom-property column returns None; a materialized column retains
        one nullable value per selected atom, including an empty list for no atoms.

    .. versionadded:: 1.0.0
    """
    return _field(item, "atom", "n_explicit_hydrogens", indices)


@arg_digest(form=form)
def get_allows_implicit_hydrogens_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored permission for implicit hydrogens.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of bool or None, or None
        Declared permission per atom; false is an available assignment, not a
        missing value.
        An absent atom-property column returns None; a materialized column retains
        one nullable value per selected atom, including an empty list for no atoms.

    .. versionadded:: 1.0.0
    """
    return _field(item, "atom", "allows_implicit_hydrogens", indices)


@arg_digest(form=form)
def get_atom_stereochemistry_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored atom stereochemistry labels.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None, or None
        Assigned stereochemistry per atom; labels are not derived from
        coordinates or connectivity.
        An absent atom-property column returns None; a materialized column retains
        one nullable value per selected atom, including an empty list for no atoms.

    .. versionadded:: 1.0.0
    """
    return _field(item, "atom", "atom_stereochemistry", indices)


@arg_digest(form=form)
def get_formal_charge_from_system(item, skip_digestion=False):
    """Reading stored integer formal charges in elementary-charge units.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None, or None
        Formal charge per atom, in integer multiples of the elementary charge;
        not a partial charge or a summed system charge.
        An absent atom-property column returns None; a materialized column retains
        one nullable value per selected atom, including an empty list for no atoms.

    .. versionadded:: 1.0.0
    """
    return _field(item, "atom", "formal_charge")


@arg_digest(form=form)
def get_bond_id_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored bond labels without interpreting them as positions.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        String labels in bond-row order; labels need not be unique and are not
        bond indices. Missing fields return one None per selected edge, or []
        for no edges.

    .. versionadded:: 1.0.0
    """
    return _field(item, "bond", "bond_id", indices)


@arg_digest(form=form)
def get_bond_order_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored integer bond orders.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        Declared integer order per edge; unknown order is not replaced with a
        single bond. Missing fields return one None per selected edge, or [] for
        no edges.

    .. versionadded:: 1.0.0
    """
    return _field(item, "bond", "bond_order", indices)


@arg_digest(form=form)
def get_fractional_bond_order_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored fractional bond orders.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of float or None
        Declared dimensionless fractional order per edge; no electronic
        calculation is performed. Missing fields return one None per selected
        edge, or [] for no edges.

    .. versionadded:: 1.0.0
    """
    return _field(item, "bond", "fractional_bond_order", indices)


@arg_digest(form=form)
def get_bond_type_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored chemical bond types.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        Declared covalent, dative or unknown type per edge; geometric proximity
        is not interpreted. Missing fields return one None per selected edge, or
        [] for no edges.

    .. versionadded:: 1.0.0
    """
    return _field(item, "bond", "bond_type", indices)


@arg_digest(form=form)
def get_bond_is_aromatic_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored bond aromaticity assignments.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of bool or None
        Declared aromaticity per edge; false remains distinct from an unknown
        assignment. Missing fields return one None per selected edge, or [] for
        no edges.

    .. versionadded:: 1.0.0
    """
    return _field(item, "bond", "bond_is_aromatic", indices)


@arg_digest(form=form)
def get_bond_is_conjugated_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored bond conjugation assignments.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of bool or None
        Declared conjugation per edge; no aromaticity or conjugation perception
        is performed. Missing fields return one None per selected edge, or []
        for no edges.

    .. versionadded:: 1.0.0
    """
    return _field(item, "bond", "bond_is_conjugated", indices)


@arg_digest(form=form)
def get_bond_stereochemistry_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored bond stereochemistry labels.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        Assigned stereochemistry per edge; no coordinate-based stereochemistry
        is inferred. Missing fields return one None per selected edge, or [] for
        no edges.

    .. versionadded:: 1.0.0
    """
    return _field(item, "bond", "bond_stereochemistry", indices)


@arg_digest(form=form)
def get_bond_stereo_atom_indices_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored atom references for bond stereochemistry.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of list of int or None
        Two independently nullable atom indices per edge, in stored reference
        order; these are not atom IDs. Missing references retain two nullable
        positions per edge; no edges returns [].

    .. versionadded:: 1.0.0
    """
    return _field(item, "bond", "bond_stereo_atom_indices", indices)


@arg_digest(form=form)
def get_bond_donor_atom_index_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored donor atom indices of directed bonds.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        Declared donor atom position per edge; undirected or unassigned edges
        remain missing. Missing fields return one None per selected edge, or []
        for no edges.

    .. versionadded:: 1.0.0
    """
    return _field(item, "bond", "bond_donor_atom_index", indices)


@arg_digest(form=form)
def get_bond_acceptor_atom_index_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored acceptor atom indices of directed bonds.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        Declared acceptor atom position per edge; no direction is inferred from
        endpoint order. Missing fields return one None per selected edge, or []
        for no edges.

    .. versionadded:: 1.0.0
    """
    return _field(item, "bond", "bond_acceptor_atom_index", indices)


@arg_digest(form=form)
def get_bond_joins_components_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored bond participation in component connectivity.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of bool or None
        Declared participation flag per edge; no components are rebuilt or flags
        synthesized during reading. Missing fields return one None per selected
        edge, or [] for no edges.

    .. versionadded:: 1.0.0
    """
    return _field(item, "bond", "bond_joins_components", indices)


@arg_digest(form=form)
def get_bond_evidence_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored evidence labels for chemical bonds.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        Original evidence declaration per edge; reading a value does not certify
        its scientific provenance. Missing fields return one None per selected
        edge, or [] for no edges.

    .. versionadded:: 1.0.0
    """
    return _field(item, "bond", "bond_evidence", indices)


@arg_digest(form=form)
def get_component_id_from_component(item, indices="all", skip_digestion=False):
    """Reading stored state-local component labels.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's component axis, retaining order and
        repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        String component labels; they are not component indices and are not
        regenerated. Missing labels retain None.

    .. versionadded:: 1.0.0
    """
    return _field(item, "component", "component_id", indices)


@arg_digest(form=form)
def get_component_id_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored state-local component labels.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        String component labels; they are not component indices and are not
        regenerated. Each atom receives its component label; unknown membership
        returns None.

    .. versionadded:: 1.0.0
    """
    return _field(item, "atom", "component_id", indices)


@arg_digest(form=form)
def get_component_name_from_component(item, indices="all", skip_digestion=False):
    """Reading stored state-local component names.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's component axis, retaining order and
        repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        Assigned component names; no molecular identity or chemical name is
        inferred. Missing labels retain None.

    .. versionadded:: 1.0.0
    """
    return _field(item, "component", "component_name", indices)


@arg_digest(form=form)
def get_component_name_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored state-local component names.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        Assigned component names; no molecular identity or chemical name is
        inferred. Each atom receives its component label; unknown membership
        returns None.

    .. versionadded:: 1.0.0
    """
    return _field(item, "atom", "component_name", indices)


@arg_digest(form=form)
def get_component_type_from_component(item, indices="all", skip_digestion=False):
    """Reading stored state-local component types.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's component axis, retaining order and
        repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        Assigned component types; no chemical classification or component
        rebuilding is performed. Missing labels retain None.

    .. versionadded:: 1.0.0
    """
    return _field(item, "component", "component_type", indices)


@arg_digest(form=form)
def get_component_type_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored state-local component types.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        Assigned component types; no chemical classification or component
        rebuilding is performed. Each atom receives its component label; unknown
        membership returns None.

    .. versionadded:: 1.0.0
    """
    return _field(item, "atom", "component_type", indices)


__all__ = [name for name in globals() if name.startswith("get_")]
