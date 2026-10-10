"""Calculating atom-aligned partial charges with an explicit scientific model."""

from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "physchem"])
@arg_digest()
@dep_digest("rdkit", when={"method": "gasteiger_marsili"})
@dep_digest("openmm", when={"method": "forcefield"})
def get_partial_charges(
    molecular_system,
    method,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    forcefield=None,
    water_model=None,
    expected_total_charge=None,
    return_report=False,
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Calculating partial charges on a complete graph before selecting atoms.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying chemical elements and state-specific
        connectivity. Source atoms, hydrogens and chemical assignments are retained.
    method : str
        Explicit 'gasteiger_marsili' (RDKit, twelve iterations) or 'forcefield'
        (OpenMM nonbonded parameters). No method or provider fallback is used.
    selection : str, list, tuple or numpy.ndarray, default='all'
        Atoms to return after calculating and validating the full graph.
        Source indices are sorted and deduplicated; selection never caps fragments.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based) for state resolution and spatial selections.
        Neither model uses coordinates to calculate charges.
    chemical_state : str or int, default='reference'
        Selected chemical state; 'structure' must resolve to one state.
    forcefield : str, default=None
        Required named force field for method='forcefield', for example 'AMBER14'.
        Must be None for Gasteiger-Marsili charges.
    water_model : str, default=None
        Optional force-field water template set. Must be None for Gasteiger-Marsili.
    expected_total_charge : int or quantity, default=None
        Declared full-system total in elementary-charge units for an integer,
        or in any charge unit for a scalar quantity. If absent, the complete
        formal-charge inventory supplies the total. Required when that inventory
        is missing. A declaration must agree with known complete formal charges.
    return_report : bool, default=False
        Return a dictionary with partial_charge and a detached report when True.
    syntax : str, default='MolSysMT'
        Syntax used for selection.
    skip_digestion : bool, default=False
        Whether to skip argument digestion.

    Returns
    -------
    quantity or dict
        Charges in configured standard charge units, shape (n_selected_atoms,).
        The optional molsysmt.partial_charge_assignment@1 report identifies
        source indices, full coverage, state, method, parameters, original software
        versions, references, and full-system total-charge check in elementary
        charge. Its numerical tolerance is 1e-6 e; this checks conservation,
        not physical accuracy. Empty selections retain shape (0,).

    Raises
    ------
    ArgumentError
        If method parameters, selections or the total-charge declaration are invalid.
    StructuralInconsistencyError
        If chemistry is incomplete or unsupported, a provider fails, particles
        differ from the source atom axis, or charges are missing, nonfinite or
        inconsistent with the declared total.
    ImportError
        If the method's explicitly required optional provider is unavailable.
    NoStandardsError
        If the active PyUnitWizard policy has no standard unit for charge.

    Notes
    -----
    Gasteiger-Marsili implements iterative partial equalization of orbital
    electronegativity (1980, DOI 10.1016/0040-4020(80)80168-2), through RDKit.
    This bounded route requires explicit indexed hydrogens, complete covalent
    connectivity, formal charges and closed-shell organic chemistry. RDKit
    sanitation perceives aromaticity and valence on a detached graph; conflicting
    declared atom aromaticity or any perceived virtual H/radical fails.
    Virtual hydrogen charges are never silently added to heavy atoms. Metals,
    radicals and query chemistry fail explicitly; no element substitutions run.
    Force-field charges use matching OpenMM templates on the unchanged graph.
    Missing hydrogens, unmatched residues and extra particles fail; this operation
    does not prepare protonation, add H or parameterize arbitrary ligands.
    Source-provided partial charges are not inputs to either calculation.
    Neither route assesses electrostatic accuracy or guarantees docking readiness.
    Optional Ackredit diagnostics cannot discard completed scientific results.
    Returning a quantity requires a standard for charge in the active
    PyUnitWizard policy; a policy containing only length and time raises
    NoStandardsError. Native build.assign_partial_charges instead stores fixed
    elementary-charge values without requiring that presentation standard.

    See Also
    --------
    molsysmt.build.assign_partial_charges : Store a validated assignment on a copy.
    get_chemical_readiness : Inspect stored chemistry before calculation.
    molsysmt.build.add_missing_hydrogens : Materialize a fixed-state H inventory.

    Examples
    --------
    >>> import molsysmt as msm
    >>> result = msm.physchem.get_partial_charges(
    ...     msm.systems['caffeine']['caffeine.sdf'], method='gasteiger_marsili',
    ...     return_report=True)
    >>> result['partial_charge'].shape
    (24,)
    >>> result['report']['coverage']
    'complete'

    .. admonition:: User guide

       See :ref:`Tutorial_Partial_Charge_Assignment` for chemistry and coverage limits.

    .. versionadded:: 1.0.0
    """
    from molsysmt import pyunitwizard as puw
    from molsysmt._private.partial_charges import calculate

    # Compatibility with the runtime floor preceding uibcdf/argdigest#17.
    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(
            skip_digestion, caller="molsysmt.physchem.get_partial_charges"
        )

    result = calculate(
        molecular_system,
        method,
        selection,
        structure_indices,
        chemical_state,
        forcefield,
        water_model,
        expected_total_charge,
        syntax,
    )
    result["partial_charge"] = puw.quantity(
        result["partial_charge"], "elementary_charge", standardized=True
    )
    return result if return_report else result["partial_charge"]
