"""Closing a declared terminal-H permission without changing its inventory."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "chemical_states", "preparation"])
@arg_digest(native_chemical_state=True)
def normalize_indexed_hydrogen_policy(
    molecular_system, chemical_state="reference", skip_digestion=False
):
    """Closing implicit-H permission on already indexed neutral terminal H.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form providing atom elements and stored chemical states.
        Native MolSys, complementary Topology/ChemicalStates domains and their
        supported converters supply the required context. ChemicalStates alone
        lacks elements and cannot identify hydrogen atoms.
    chemical_state : int, {'reference'}, or None, default='reference'
        Positional state or the resolved reference. Other states and structure
        associations are retained. None selects the reference. This operation
        is independent of structures; 'structure' is not a supported selector.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    dict
        Independent native molecular_system and a detached
        molsysmt.indexed_hydrogen_policy@1 report. Its method is
        closed_neutral_terminal_hydrogens. Sorted int64 hydrogen_atom_indices,
        changed_atom_indices, parent_hydrogen_pairs and original Boolean flags
        retain the source axis. The compact atom_correspondence declares
        identity and n_atoms instead of allocating every identity pair.
        Status is normalized, unchanged or empty. The selected state's history
        receives an independent copy, including successful no-op calls.

    Raises
    ------
    ArgumentError
        If the state selector is malformed or uses 'structure'.
    StructuralInconsistencyError
        If element/state context, complete supported connectivity or known H
        inventory is unavailable, or an indexed H is outside the declared profile.
        Validation completes before preparing a result; the source is preserved.

    Notes
    -----
    This experimental MolSysMT representation policy changes only
    allows_implicit_hydrogens to False on already indexed H atoms. The public
    hydrogen-inventory audit must be available: connectivity is complete, bonds
    are ordinary covalent relationships, all stored virtual-H counts are known,
    and every indexed H has exactly one non-H parent and zero virtual H.
    Each H additionally needs known zero formal charge/radical count, known
    nonaromaticity, unspecified atom stereo and a known single nonaromatic bond
    without bond stereo. Unknown or incompatible assignments reject. Isotope
    labels, including deuterium and tritium, are preserved.

    No atoms, bonds, H counts, heavy-atom permissions or other stereochemical
    assignments are changed. Native coordinate quantities retain their values
    and units; foreign conversion follows its existing reader/unit contract.
    The policy does not examine geometry or change the caller's unit policy. This neither
    predicts protonation nor certifies valence, coordinate quality, chemical
    equivalence or the suitability of a molecular model. Strict correspondence
    still compares the stored labels; it does not invoke this policy implicitly.

    Native MolSys.copy(deep=False) detaches chemistry and mutable metadata while
    sharing protected coordinate/box blocks until controlled edits replace
    affected blocks. No coordinate structure is examined for admission. Foreign
    conversion, including a complete H5MSM load, may materialize coordinates.
    Changed chemistry invalidates named analyses on the returned system through
    the chemical owner; unchanged/empty results retain their coverage. Source
    analyses are preserved. Historical indices keep the original operation
    domain after later extraction or reordering. Typed ChemicalStatesDict and
    H5MSM preserve the report and the software version that produced it.

    See Also
    --------
    molsysmt.physchem.get_hydrogen_inventory
        Audit indexed neighbors and stored virtual counts without changing them.
    get_atom_correspondences
        Compare declared chemical states without implicit normalization.
    molsysmt.build.add_missing_hydrogens
        Materialize a declared inventory through explicit fixed-state preparation.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert('smiles:[2H]O')
    >>> msm.set(molsys, selection="atom_type=='H'", allows_implicit_hydrogens=True)
    >>> result = msm.chemical_states.normalize_indexed_hydrogen_policy(molsys)
    >>> result['report']['hydrogen_atom_indices'].size
    1
    >>> result['report']['atom_correspondence']['indices']
    'identity'

    .. admonition:: User guide

       See :ref:`Tutorial_Normalize_Indexed_Hydrogen_Policy` for scope and history.

    .. versionadded:: 1.0.0
    """
    from ._indexed_hydrogen_policy import normalize

    return normalize(
        molecular_system,
        chemical_state,
        "molsysmt.chemical_states.normalize_indexed_hydrogen_policy",
    )
