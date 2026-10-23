"""Reducing an explicitly typed atom representation without recalculating charges."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "build"])
@arg_digest()
def merge_nonpolar_hydrogens(
    molecular_system,
    typing_scheme,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    return_report=False,
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Merging explicitly typed nonpolar H into their retained bonded parents.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying a complete single chemical state, elements,
        indexed H, finite partial charges and explicit AutoDock4 labels.
    typing_scheme : str
        Required explicit 'autodock4' vocabulary. H labels are merged; HD labels
        are retained. Atom names never determine this decision.
    selection : str, list, tuple or numpy.ndarray, default='all'
        Source atoms to project. Sorted and deduplicated. A merged H and its
        parent must both belong to this selection; other source atoms are omitted.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based) to retain, in native extraction order.
    chemical_state : str or int, default='reference'
        Selected single state; 'structure' resolves the selected structures.
    return_report : bool, default=False
        Return molecular_system and a detached atom-projection report when True.
    syntax : str, default='MolSysMT'
        Syntax used for selection.
    skip_digestion : bool, default=False
        Whether to skip argument digestion.

    Returns
    -------
    molsysmt.MolSys or dict
        Detached reduced MolSys, optionally accompanied by report with schema
        molsysmt.atom_projection@1. Maps use source/output indices, -1 for absent
        direct correspondence, and separate merged H/parent pairs. Charge
        transfers and totals carry charge_unit='elementary_charge'.

    Raises
    ------
    ArgumentError
        If the scheme, selection or structure request is invalid.
    StructuralInconsistencyError
        If chemistry, types, charge bindings or parent inventory are unavailable
        or inconsistent, or an H has no unique retained single-bonded parent.

    Notes
    -----
    Terminal neutral, nonradical, nonisotopic H with AutoDock4 type H transfer
    their full stored partial charge to the bonded parent. This follows the
    terminal charge-aggregation approach inspected in Meeko 0.8.0; its code is
    not copied and Meeko is not a dependency. Types and charges are never
    calculated here. The original charge calculation remains nested provenance;
    the new assignment is explicitly a derived aggregation, not a new calculation.
    Parent virtual explicit-H counts increase; known zero implicit-H counts
    are required, and further implicit-H inference is disabled for those parents.
    Unknown parent counts must be declared or prepared separately.
    The source is unchanged. Reduced interaction analyses are cleared after a
    merge. General force-field settings beyond atom types/charges are rejected;
    this operation does not derive a united-atom force field. Copying selected
    structures is resident, not streaming. Mechanical provenance is not H5MSM 0.5.

    See Also
    --------
    assign_autodock_atom_types : Attach a named chemical typing profile.
    assign_partial_charges : Calculate and attach the original charge assignment.
    molsysmt.physchem.get_hydrogen_inventory : Inspect virtual and indexed counts.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['caffeine']['caffeine.sdf'], to_form='rdkit.Mol')
    >>> molsys = msm.build.assign_autodock_atom_types(molsys, typing_scheme='autodock4')
    >>> molsys = msm.build.assign_partial_charges(molsys, method='gasteiger_marsili')
    >>> reduced = msm.build.merge_nonpolar_hydrogens(molsys, typing_scheme='autodock4')
    >>> reduced.get_n_atoms()
    14

    .. admonition:: User guide

       See :ref:`Tutorial_Merge_Nonpolar_Hydrogens` for prerequisites and maps.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.hydrogen_projection import project

    return project(
        molecular_system,
        typing_scheme,
        selection,
        structure_indices,
        chemical_state,
        return_report,
        syntax,
    )
