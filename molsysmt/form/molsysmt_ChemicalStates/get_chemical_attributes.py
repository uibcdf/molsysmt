"""Deliver stored chemical fields from the active ChemicalStates scope."""

from molsysmt._private.argdigest import arg_digest
from molsysmt.native._chemical_fields import field as _field

form = "molsysmt.ChemicalStates"


@arg_digest(form=form)
def get_formal_charge_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored integer formal charges in elementary-charge units.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference chemical state.
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
