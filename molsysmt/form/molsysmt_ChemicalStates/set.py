"""Assign stored atom/bond fields through the selected chemical-state owner."""

from molsysmt._private.argdigest import arg_digest
from molsysmt.native._chemical_assignments import assign_field as _assign

form = "molsysmt.ChemicalStates"


@arg_digest(form=form)
def set_formal_charge_to_atom(item, indices="all", value=None, skip_digestion=False):
    """Setting integer formal charges in elementary-charge units.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's atom domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        An integer count or aligned nullable vector, or a one-dimensional charge
        quantity converted explicitly to elementary charge. Unselected atoms retain
        their assignments.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. Scientific assignments conservatively
    invalidate all named analyses of an owning MolSys, including evaluated-empty
    structures.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> msm.set(chemical_states, element='atom', selection=[1], formal_charge=-1)
    >>> chemical_states.get(element='atom', formal_charge=True)
    [None, -1]

    .. versionadded:: 1.0.0
    """
    _assign(item, "formal_charge", value, indices)


@arg_digest(form=form)
def set_atom_is_aromatic_to_atom(item, indices="all", value=None, skip_digestion=False):
    """Setting declared atom aromaticity.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's atom domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        A boolean or aligned nullable boolean vector. This stores an assignment and does
        not perceive aromaticity.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. Scientific assignments conservatively
    invalidate all named analyses of an owning MolSys, including evaluated-empty
    structures.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> msm.set(chemical_states, element='atom', selection=[1], atom_is_aromatic=True)
    >>> chemical_states.get(element='atom', atom_is_aromatic=True)
    [None, True]

    .. versionadded:: 1.0.0
    """
    _assign(item, "atom_is_aromatic", value, indices)


@arg_digest(form=form)
def set_n_unpaired_electrons_to_atom(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting declared unpaired-electron counts.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's atom domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        A nonnegative integer count or aligned nullable vector, representable as UInt8.
        No radical-state inference runs.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. Scientific assignments conservatively
    invalidate all named analyses of an owning MolSys, including evaluated-empty
    structures.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> msm.set(chemical_states, element='atom', selection=[1], n_unpaired_electrons=1)
    >>> chemical_states.get(element='atom', n_unpaired_electrons=True)
    [None, 1]

    .. versionadded:: 1.0.0
    """
    _assign(item, "n_unpaired_electrons", value, indices)


@arg_digest(form=form)
def set_n_implicit_hydrogens_to_atom(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting declared implicit-hydrogen counts.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's atom domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        A nonnegative integer count or aligned nullable vector, representable as UInt8.
        No atoms or bonds are added.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. Scientific assignments conservatively
    invalidate all named analyses of an owning MolSys, including evaluated-empty
    structures.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> msm.set(chemical_states, element='atom', selection=[1], n_implicit_hydrogens=1)
    >>> chemical_states.get(element='atom', n_implicit_hydrogens=True)
    [None, 1]

    .. versionadded:: 1.0.0
    """
    _assign(item, "n_implicit_hydrogens", value, indices)


@arg_digest(form=form)
def set_n_explicit_hydrogens_to_atom(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting declared explicit-hydrogen counts.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's atom domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        A nonnegative integer count or aligned nullable vector, representable as UInt8.
        These declarations do not recount bonded hydrogen atoms.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. Scientific assignments conservatively
    invalidate all named analyses of an owning MolSys, including evaluated-empty
    structures.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> msm.set(chemical_states, element='atom', selection=[1], n_explicit_hydrogens=1)
    >>> chemical_states.get(element='atom', n_explicit_hydrogens=True)
    [None, 1]

    .. versionadded:: 1.0.0
    """
    _assign(item, "n_explicit_hydrogens", value, indices)


@arg_digest(form=form)
def set_allows_implicit_hydrogens_to_atom(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting permission for implicit hydrogens.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's atom domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        A boolean or aligned nullable boolean vector. False forbids implicit hydrogens;
        it is distinct from an unknown permission.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. Scientific assignments conservatively
    invalidate all named analyses of an owning MolSys, including evaluated-empty
    structures.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> msm.set(chemical_states, element='atom', selection=[1], allows_implicit_hydrogens=False)
    >>> chemical_states.get(element='atom', allows_implicit_hydrogens=True)
    [None, False]

    .. versionadded:: 1.0.0
    """
    _assign(item, "allows_implicit_hydrogens", value, indices)


@arg_digest(form=form)
def set_atom_stereochemistry_to_atom(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting declared atom stereochemistry.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's atom domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        An R, S, r, s, unspecified or unknown label, or an aligned nullable vector. No
        coordinate-based stereochemistry is perceived.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. Scientific assignments conservatively
    invalidate all named analyses of an owning MolSys, including evaluated-empty
    structures.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> msm.set(chemical_states, element='atom', selection=[1], atom_stereochemistry='R')
    >>> chemical_states.get(element='atom', atom_stereochemistry=True)
    [None, 'R']

    .. versionadded:: 1.0.0
    """
    _assign(item, "atom_stereochemistry", value, indices)


@arg_digest(form=form)
def set_bond_id_to_bond(item, indices="all", value=None, skip_digestion=False):
    """Setting string labels on stored bond positions.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's bond domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        A scalar label or aligned nullable vector; numeric labels become strings. Labels
        need not be unique and do not select bond rows.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. String-label edits preserve interaction
    observations and bond-row layout.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> chemical_states.add_bonds([[0, 1]])
    >>> msm.set(chemical_states, element='bond', bond_id=19)
    >>> chemical_states.get(element='bond', bond_id=True)
    ['19']

    .. versionadded:: 1.0.0
    """
    _assign(item, "bond_id", value, indices)


@arg_digest(form=form)
def set_bond_order_to_bond(item, indices="all", value=None, skip_digestion=False):
    """Setting integer orders of stored bonds.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's bond domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        An integer from 0 to 255 or an aligned nullable vector. Edges are not added or
        removed.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. Scientific assignments conservatively
    invalidate all named analyses of an owning MolSys, including evaluated-empty
    structures.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> chemical_states.add_bonds([[0, 1]])
    >>> msm.set(chemical_states, element='bond', bond_order=2)
    >>> chemical_states.get(element='bond', bond_order=True)
    [2]

    .. versionadded:: 1.0.0
    """
    _assign(item, "bond_order", value, indices)


@arg_digest(form=form)
def set_fractional_bond_order_to_bond(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting dimensionless fractional bond orders.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's bond domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        A finite nonnegative real value or aligned nullable vector. No electronic
        calculation runs.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. Scientific assignments conservatively
    invalidate all named analyses of an owning MolSys, including evaluated-empty
    structures.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> chemical_states.add_bonds([[0, 1]])
    >>> msm.set(chemical_states, element='bond', fractional_bond_order=1.5)
    >>> chemical_states.get(element='bond', fractional_bond_order=True)
    [1.5]

    .. versionadded:: 1.0.0
    """
    _assign(item, "fractional_bond_order", value, indices)


@arg_digest(form=form)
def set_bond_type_to_bond(item, indices="all", value=None, skip_digestion=False):
    """Setting declared chemical bond types.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's bond domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        A covalent, dative or unknown label, or an aligned nullable vector. Existing
        canonical participation/evidence validation applies.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. Scientific assignments conservatively
    invalidate all named analyses of an owning MolSys, including evaluated-empty
    structures.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> chemical_states.add_bonds([[0, 1]])
    >>> msm.set(chemical_states, element='bond', bond_type='dative')
    >>> chemical_states.get(element='bond', bond_type=True)
    ['dative']

    .. versionadded:: 1.0.0
    """
    _assign(item, "bond_type", value, indices)


@arg_digest(form=form)
def set_bond_is_aromatic_to_bond(item, indices="all", value=None, skip_digestion=False):
    """Setting declared bond aromaticity.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's bond domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        A boolean or aligned nullable boolean vector. This records an assignment without
        aromaticity perception.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. Scientific assignments conservatively
    invalidate all named analyses of an owning MolSys, including evaluated-empty
    structures.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> chemical_states.add_bonds([[0, 1]])
    >>> msm.set(chemical_states, element='bond', bond_is_aromatic=True)
    >>> chemical_states.get(element='bond', bond_is_aromatic=True)
    [True]

    .. versionadded:: 1.0.0
    """
    _assign(item, "bond_is_aromatic", value, indices)


@arg_digest(form=form)
def set_bond_is_conjugated_to_bond(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting declared bond conjugation.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's bond domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        A boolean or aligned nullable boolean vector. This records an assignment without
        conjugation perception.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. Scientific assignments conservatively
    invalidate all named analyses of an owning MolSys, including evaluated-empty
    structures.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> chemical_states.add_bonds([[0, 1]])
    >>> msm.set(chemical_states, element='bond', bond_is_conjugated=False)
    >>> chemical_states.get(element='bond', bond_is_conjugated=True)
    [False]

    .. versionadded:: 1.0.0
    """
    _assign(item, "bond_is_conjugated", value, indices)


@arg_digest(form=form)
def set_bond_stereochemistry_to_bond(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting declared bond stereochemistry.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's bond domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        A canonical stereochemistry label or aligned nullable vector. Assign required
        stereo atom references first; invalid combinations reject before publication.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. Scientific assignments conservatively
    invalidate all named analyses of an owning MolSys, including evaluated-empty
    structures.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> chemical_states.add_bonds([[0, 1]])
    >>> msm.set(chemical_states, element="bond", bond_stereo_atom_indices=[0, 1])
    >>> msm.set(chemical_states, element='bond', bond_stereochemistry='E')
    >>> chemical_states.get(element='bond', bond_stereochemistry=True)
    ['E']

    .. versionadded:: 1.0.0
    """
    _assign(item, "bond_stereochemistry", value, indices)


@arg_digest(form=form)
def set_bond_stereo_atom_indices_to_bond(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting both stereo atom references of stored bonds.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's bond domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        An array with shape (n_selected_bonds, 2) of nullable atom indices. A single
        selected bond also accepts a two-element vector. Both columns are validated and
        published together.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. Scientific assignments conservatively
    invalidate all named analyses of an owning MolSys, including evaluated-empty
    structures.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> chemical_states.add_bonds([[0, 1]])
    >>> msm.set(chemical_states, element='bond', bond_stereo_atom_indices=[0, 1])
    >>> chemical_states.get(element='bond', bond_stereo_atom_indices=True)
    [[0, 1]]

    .. versionadded:: 1.0.0
    """
    _assign(item, "bond_stereo_atom_indices", value, indices)


@arg_digest(form=form)
def set_bond_donor_atom_index_to_bond(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting directed-bond donor atom references.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's bond domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        A nullable atom index or aligned vector, referencing a stored endpoint. Known
        donor and acceptor indices must be distinct.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. Scientific assignments conservatively
    invalidate all named analyses of an owning MolSys, including evaluated-empty
    structures.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> chemical_states.add_bonds([[0, 1]])
    >>> msm.set(chemical_states, element='bond', bond_donor_atom_index=0)
    >>> chemical_states.get(element='bond', bond_donor_atom_index=True)
    [0]

    .. versionadded:: 1.0.0
    """
    _assign(item, "bond_donor_atom_index", value, indices)


@arg_digest(form=form)
def set_bond_acceptor_atom_index_to_bond(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting directed-bond acceptor atom references.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's bond domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        A nullable atom index or aligned vector, referencing a stored endpoint. Known
        donor and acceptor indices must be distinct.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. Scientific assignments conservatively
    invalidate all named analyses of an owning MolSys, including evaluated-empty
    structures.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> chemical_states.add_bonds([[0, 1]])
    >>> msm.set(chemical_states, element='bond', bond_acceptor_atom_index=1)
    >>> chemical_states.get(element='bond', bond_acceptor_atom_index=True)
    [1]

    .. versionadded:: 1.0.0
    """
    _assign(item, "bond_acceptor_atom_index", value, indices)


@arg_digest(form=form)
def set_bond_joins_components_to_bond(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting declared bond participation in connectivity.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's bond domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        A nullable boolean or aligned vector. Nondefault participation needs evidence;
        assigning this flag does not rebuild components.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. Scientific assignments conservatively
    invalidate all named analyses of an owning MolSys, including evaluated-empty
    structures.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> chemical_states.add_bonds([[0, 1]])
    >>> msm.set(chemical_states, element="bond", bond_evidence="explicit")
    >>> msm.set(chemical_states, element='bond', bond_joins_components=False)
    >>> chemical_states.get(element='bond', bond_joins_components=True)
    [False]

    .. versionadded:: 1.0.0
    """
    _assign(item, "bond_joins_components", value, indices)


@arg_digest(form=form)
def set_bond_evidence_to_bond(item, indices="all", value=None, skip_digestion=False):
    """Setting evidence declarations on stored bonds.

    Parameters
    ----------
    item : molsysmt.ChemicalStates
        Collection with an unambiguous active or reference state. Public
        msm.set selects its state with chemical_state without changing the reference.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the active state's bond domain. Empty selections are
        no-ops after state resolution; missing or invalid positions reject.
    value : scalar or array-like, default=None
        An explicit, inferred, user_defined or unknown label, or an aligned nullable
        vector. This declaration does not authenticate scientific provenance.
        Missing entries assign unknown values rather than inferring replacements.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    One attribute is staged and validated before publication. A failed assignment
    preserves source tables and analyses. Other states, coordinates, history and
    structure associations are retained. Scientific assignments conservatively
    invalidate all named analyses of an owning MolSys, including evaluated-empty
    structures.
    No chemical state, coordinate, edge or component is created automatically.
    A basic.set call with several attributes performs separate assignments.

    Examples
    --------
    >>> import molsysmt as msm
    >>> chemical_states = msm.ChemicalStates(n_atoms=2)
    >>> chemical_states.append_state()
    0
    >>> chemical_states.add_bonds([[0, 1]])
    >>> msm.set(chemical_states, element='bond', bond_evidence='explicit')
    >>> chemical_states.get(element='bond', bond_evidence=True)
    ['explicit']

    .. versionadded:: 1.0.0
    """
    _assign(item, "bond_evidence", value, indices)


__all__ = [name for name in globals() if name.startswith("set_")]
