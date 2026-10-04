"""Attaching a named charge assignment without changing molecular chemistry."""

from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "build"])
@arg_digest()
@dep_digest("rdkit", when={"method": "gasteiger_marsili"})
@dep_digest("openmm", when={"method": "forcefield"})
def assign_partial_charges(
    molecular_system,
    method,
    structure_indices="all",
    chemical_state="reference",
    forcefield=None,
    water_model=None,
    expected_total_charge=None,
    return_report=False,
    skip_digestion=False,
):
    """Assigning validated full-atom charges to a detached single-state MolSys.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form providing the selected model's chemical prerequisites.
        Exactly one chemical state is required for native mechanical storage.
    method : str
        Explicit 'gasteiger_marsili' or 'forcefield' charge model.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based) for resolving chemical_state='structure'.
        All source structures are retained; coordinates are not used by the model.
    chemical_state : str or int, default='reference'
        State to calculate. Multi-state inputs must first be reduced explicitly;
        the experimental MolecularMechanics store holds one assignment.
    forcefield : str, default=None
        Required named force field for method='forcefield'; otherwise None.
    water_model : str, default=None
        Optional force-field water template set; otherwise None.
    expected_total_charge : int or quantity, default=None
        Full-system total declaration, as an integer in elementary charge or a
        scalar charge quantity. Complete formal charges supply it when absent.
    return_report : bool, default=False
        Return the new molecular_system and its detached report when True.
    skip_digestion : bool, default=False
        Whether to skip argument digestion.

    Returns
    -------
    molsysmt.MolSys or dict
        New MolSys retaining atoms, IDs, chemistry, coordinates and named analyses.
        Its molecular_mechanics stores full atom-aligned partial_charge values in
        elementary charge and partial_charge_assignment provenance. A report is
        returned separately when requested. The source is unchanged on failure.

    Raises
    ------
    ArgumentError
        If a method parameter or state request is invalid.
    StructuralInconsistencyError
        If more than one state is present or the calculation cannot provide a
        finite, complete, total-charge-consistent assignment.
    ImportError
        If the explicitly required optional provider is unavailable.

    Notes
    -----
    Delegates the scientific calculation to physchem.get_partial_charges.
    Named analyses retain their original snapshots. As with other mechanics edits,
    callers must explicitly invalidate/recalculate analyses that depend on those
    parameters; native automatic coupling covers geometry and ChemicalStates.
    Replaces existing charges explicitly; it does not assign force-field atom types
    or other force-field parameters. A force-field charge calculation is not full
    parameterization of MolecularMechanics. Assignment provenance is retained by
    native copying and extraction; extracted charges are a projection of the
    original calculation, not a new isolated-fragment calculation. The PDBQT writer
    checks a stored assignment against its bound chemistry and values before use.
    Direct manual charge replacement clears this attribution. MolecularMechanics
    remains experimental and is excluded from H5MSM 0.5 (planned for 0.6).
    Native attachment copies the complete system, including source coordinates;
    it does not offer out-of-core trajectory assignment.

    See Also
    --------
    molsysmt.physchem.get_partial_charges : Calculate without attaching charges.

    Examples
    --------
    >>> import molsysmt as msm
    >>> output = msm.build.assign_partial_charges(
    ...     msm.systems['caffeine']['caffeine.sdf'], method='gasteiger_marsili')
    >>> output.molecular_mechanics.partial_charge_assignment['method']
    'gasteiger_marsili'

    .. admonition:: User guide

       See :ref:`Tutorial_Partial_Charge_Assignment` for assignment and export rules.

    .. versionadded:: 1.0.0
    """
    from molsysmt import pyunitwizard as puw
    from molsysmt._private.partial_charges import bind_assignment
    from molsysmt._private.smonitor import StructuralInconsistencyError
    from molsysmt.basic import convert, get_form
    from molsysmt.physchem import get_partial_charges

    # Compatibility with the runtime floor preceding uibcdf/argdigest#17.
    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(
            skip_digestion, caller="molsysmt.build.assign_partial_charges"
        )

    # The RDKit adapter calculates chemical properties on its input. Preserve
    # the public read-only boundary by detaching before form conversion.
    if get_form(molecular_system) == "rdkit.Mol":
        from rdkit import Chem

        molecular_system = Chem.Mol(molecular_system)
    source = convert(molecular_system, to_form="molsysmt.MolSys")
    if source.chemical_states is None or source.chemical_states.n_chemical_states != 1:
        raise StructuralInconsistencyError(
            reason="Charge assignment storage requires exactly one chemical state; calculate detached results for multi-state inputs.",
            caller="molsysmt.build.assign_partial_charges",
        )
    result = get_partial_charges(
        source,
        method=method,
        chemical_state=chemical_state,
        structure_indices=structure_indices,
        forcefield=forcefield,
        water_model=water_model,
        expected_total_charge=expected_total_charge,
        return_report=True,
    )
    source.molecular_mechanics.partial_charge = puw.get_value(
        result["partial_charge"], to_unit="elementary_charge"
    )
    source.molecular_mechanics.partial_charge_assignment = bind_assignment(
        source, result["report"]
    )
    return (
        {"molecular_system": source, "report": result["report"]}
        if return_report
        else source
    )
