"""Attaching declared atoms to existing parents without changing existing coordinates."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "build"])
@arg_digest()
def add_terminal_atoms(
    molecular_system,
    new_atoms,
    coordinates,
    attribute_policy="intersection",
    skip_digestion=False,
):
    """Adding terminal atoms to existing groups in a new native system.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form providing topology, one chemical state and coordinates.
    new_atoms : list or tuple
        Detached atom records. Each requires parent_atom_index (an existing
        zero-based index) and atom_type (element symbol). Optional atom_name,
        atom_id, isotope, bond_order (1, 2 or 3) and chemical_attributes declare
        identity, the parent bond and canonical ChemicalStates atom fields.
        Membership is inherited from the parent; IDs are normalized to strings.
    coordinates : quantity
        Coordinates of the added atoms, shape (n_structures, n_new_atoms, 3),
        in units of length. Every source structure must be covered.
    attribute_policy : {'intersection', 'strict'}, default='intersection'
        Intersection drops unsupported velocities, occupancies, B-factors,
        system observables and force-field parameters with a diagnostic.
        Strict rejects those inputs. Sparse alternate locations remain attached
        to the existing atom indices. No values are fabricated for new atoms.
    skip_digestion : bool, default=False
        Whether to skip argument digestion.

    Returns
    -------
    dict
        New native molecular_system and detached terminal_attachment@1 report
        with int64 old/new atom_correspondence and parent_atom_pairs, generated
        string IDs, dropped attributes and invalidated named interactions.

    Raises
    ------
    ArgumentError
        If atom records or coordinate units are invalid.
    StructuralInconsistencyError
        If axes, membership, IDs or the selected attribute policy are incompatible.

    Notes
    -----
    Existing atom indices, coordinates and chemical assignments are preserved.
    Each added atom has one covalent bond to an existing parent. This tool does
    not predict chemistry, generate coordinates or accept multiple chemical states.
    Named analyses retain provenance but become unevaluated on the returned copy;
    added atoms have no original source index. Failure leaves the source unchanged.
    Empty addition returns an independent unchanged copy with no invalidation.
    Successful attachment, including empty addition, archives an independent
    report in output ChemicalStates preparation history. It declares all examined
    structure indices, original source counts, supplied-coordinate evidence,
    attribute policy and the producing MolSysMT version. H5MSM preserves that
    evidence without embedding coordinate arrays in the report. Historical
    indices retain the operation's domain after extraction or reordering.

    See Also
    --------
    add_missing_hydrogens : Generate H coordinates for a prepared chemical state.

    Examples
    --------
    >>> import molsysmt as msm
    >>> builder = msm.MolSysBuilder()
    >>> _ = builder.add_atom(atom_type='C', atom_name='C')
    >>> builder.set_coordinates(msm.pyunitwizard.quantity([[[0., 0., 0.]]], 'nm'))
    >>> result = msm.build.add_terminal_atoms(builder.build(),
    ...     [{'parent_atom_index': 0, 'atom_type': 'H'}],
    ...     msm.pyunitwizard.quantity([[[0., 0., 0.109]]], 'nm'))
    >>> result['molecular_system'].get_n_atoms()
    2

    .. admonition:: User guide

       See :ref:`Tutorial_Add_Terminal_Atoms` for attachment and attribute policies.

    .. versionadded:: 1.0.0
    """
    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(skip_digestion, caller=__name__ + ".add_terminal_atoms")
    from molsysmt._private.terminal_atoms import attach
    from molsysmt.basic import convert
    from molsysmt.native import MolSys

    source = (
        molecular_system
        if isinstance(molecular_system, MolSys)
        else convert(molecular_system, to_form="molsysmt.MolSys")
    )
    return attach(
        source,
        new_atoms,
        coordinates,
        attribute_policy,
        "molsysmt.build.add_terminal_atoms",
    )
