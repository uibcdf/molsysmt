"""Attaching full named chemical AutoDock typing to a detached native system."""

from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "build"])
@arg_digest()
@dep_digest("rdkit")
def assign_autodock_atom_types(
    molecular_system,
    typing_scheme,
    structure_indices="all",
    chemical_state="reference",
    method="chemical_environment",
    return_report=False,
    skip_digestion=False,
):
    """Assigning full named AutoDock labels to a detached single-state MolSys.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form with the chosen profile's prerequisites. Exactly one
        nonempty chemical state is required for current mechanical storage.
    typing_scheme : str
        Required explicit 'autodock4' parameter vocabulary.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based) for resolving a structure-associated state.
        All source structures are retained, without using coordinates for typing.
    chemical_state : str or int, default='reference'
        State to classify. Reduce multi-state inputs explicitly before attachment.
    method : str, default='chemical_environment'
        Experimental chemical_environment@1 profile with auditable rule precedence.
    return_report : bool, default=False
        Return molecular_system and detached report when True.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys or dict
        New system retaining source atoms, IDs, structures, chemical assignments,
        partial charges and named analyses. Its molecular_mechanics holds
        atom_ff_type labels and atom_type_assignment provenance. The source is
        unchanged. This does not establish complete force-field parameterization.

    Raises
    ------
    ArgumentError
        If a method, scheme, state or frame request is invalid.
    StructuralInconsistencyError
        If there is no nonempty single state or the profile cannot classify all
        atoms without guessing missing chemistry or adding virtual H.
    ImportError
        If the optional RDKit provider is unavailable.

    Notes
    -----
    Calls physchem.get_autodock_atom_types; chemistry remains owned by ChemicalStates.
    The mechanical type report binds ordered labels to source chemistry/state.
    Copy/pickle preserve original producer versions. Extraction retains parent
    labels with projected provenance; it does not classify isolated fragments.
    The PDBQT writer rejects stale named chemistry/labels or a different scheme.
    Native property replacement clears named typing attribution. Existing analyses
    keep their snapshots; callers invalidate analyses depending on changed mechanics.
    Complete native copying can materialize structures; this is not streaming.
    MolecularMechanics remains experimental and is excluded from H5MSM 0.5.
    Charge calculation, H merging and docking protocols remain separate operations.

    See Also
    --------
    molsysmt.physchem.get_autodock_atom_types : Calculate without attachment.
    molsysmt.build.assign_partial_charges : Attach a separately named charge model.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.build.assign_autodock_atom_types(
    ...     msm.systems['caffeine']['caffeine.sdf'], typing_scheme='autodock4')
    >>> molsys.molecular_mechanics.atom_type_assignment['typing_scheme']
    'autodock4'

    .. admonition:: User guide

       See :ref:`Tutorial_Assign_AutoDock_Types` for attachment and export rules.

    .. versionadded:: 1.0.0
    """
    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(
            skip_digestion, caller=__name__ + ".assign_autodock_atom_types"
        )
    from molsysmt._private.autodock_assignment import bind_assignment, fail
    from molsysmt.basic import convert, get_form
    from molsysmt.physchem import get_autodock_atom_types

    if get_form(molecular_system) == "rdkit.Mol":
        from rdkit import Chem

        if any(atom.HasQuery() for atom in molecular_system.GetAtoms()) or any(
            bond.HasQuery() for bond in molecular_system.GetBonds()
        ):
            fail("AutoDock typing requires a concrete graph, not query atoms or bonds.")
        molecular_system = Chem.Mol(molecular_system)
    output = convert(molecular_system, to_form="molsysmt.MolSys")
    if (
        output.chemical_states is None
        or output.chemical_states.n_chemical_states != 1
        or not output.get_n_atoms()
    ):
        fail(
            "AutoDock type storage requires one nonempty chemical state; use detached results otherwise."
        )
    result = get_autodock_atom_types(
        output,
        typing_scheme=typing_scheme,
        structure_indices=structure_indices,
        chemical_state=chemical_state,
        method=method,
        return_report=True,
    )
    output.molecular_mechanics.atom_ff_type = result["atom_ff_type"]
    output.molecular_mechanics.atom_type_assignment = bind_assignment(
        output, result["report"]
    )
    return (
        dict(molecular_system=output, report=result["report"])
        if return_report
        else output
    )
