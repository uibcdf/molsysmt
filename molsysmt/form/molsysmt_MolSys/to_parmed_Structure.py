from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.MolSys")
@dep_digest("parmed")
def to_parmed_Structure(
    item, atom_indices="all", skip_digestion=False, *, structure_indices="all"
):
    """
    Converting native inventory, reference chemistry and structures to ParmEd.


    Parameters
    ----------
    item : molecular system
        Native system supplying stable inventory, reference ChemicalStates,
        optional structures and available molecular-mechanics atom parameters.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structures to retain, preserving the requested order and repetitions.
        This argument is keyword-only.

    Returns
    -------
    parmed.Structure
        Detached object with selected coordinates and canonical cells. ParmEd
        stores lengths in angstroms, angles in degrees and charges in elementary
        charge units. Force-field parameters are not inferred.

    Raises
    ------
    LibraryNotFoundError
        If the optional ParmEd provider is unavailable.
    NotCompatibleConversionError
        If labels, numeric bond orders, partial charges, box orientation or
        structure-to-state associations cannot be represented faithfully.

    Notes
    -----
    Unknown formal charges and atom aromaticity remain unknown. Reference-state
    chemistry is exported once; the target does not store a chemical-state
    collection. Use ``molsysmt.convert(..., strict=True)`` or ``return_report=True``
    to inspect additional source semantics omitted by this representation.

    Examples
    --------
    >>> from molsysmt.native import MolSys
    >>> converted = to_parmed_Structure(MolSys())
    >>> len(converted.atoms)
    0


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.parmed_Structure._from_native import (
        export_native,
        reject_limitations,
        state_association_limitations,
    )

    from .extract import extract

    selected = extract(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        copy_if_all=False,
        skip_digestion=True,
    )
    reject_limitations(state_association_limitations(selected), "molsysmt.MolSys")
    return export_native(
        selected.topology,
        chemical_states=selected.chemical_states,
        structures=selected.structures,
        molecular_mechanics=selected.molecular_mechanics,
    )
