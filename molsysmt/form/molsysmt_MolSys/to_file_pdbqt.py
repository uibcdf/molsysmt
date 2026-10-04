from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.MolSys")
def to_file_pdbqt(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    skip_digestion=False,
    *,
    typing_scheme=None,
    torsion_tree=None,
):
    """Writing one native structure as explicit AutoDock4 PDBQT data.

    Parameters
    ----------
    item : molsysmt.MolSys
        Native system with explicit coordinates, partial charges and AutoDock types.
    atom_indices : int, list, tuple or numpy.ndarray, default='all'
        Atom indices (0-based) to include. A supplied tree must match the selected axis.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based). Exactly one must be selected.
    output_filename : str or pathlib.Path, default=None
        Destination path, required for file output. Opened only after validation.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.
    typing_scheme : str or None, default=None
        Keyword-only explicit 'autodock4' declaration. None fails; labels are
        validated against chemical element symbols, without assigning them.
    torsion_tree : dict or None, default=None
        Keyword-only molsysmt.pdbqt-torsion-tree@1 dictionary bound to selected
        atom IDs and order. None writes a rigid receptor; a tree writes a ligand.

    Returns
    -------
    str or pathlib.Path
        Destination path.

    Raises
    ------
    FormatError
        For missing charges/types/coordinates, invalid field widths or tree,
        unsupported isotopes, nonnumeric atom IDs or multiple selected frames.
    StructuralInconsistencyError
        For named charge/type assignments that no longer match bound chemistry,
        ordered values, associated chemical state or requested typing scheme.

    Notes
    -----
    Coordinates are explicitly converted to angstroms, independent of the
    session unit policy; charges are native values in elementary charge.
    Every input hydrogen is retained. No hydrogen merging, charge aggregation,
    typing, rotatable-bond perception or molecular preparation is performed.
    Atom serial IDs are preserved. Tree serialization traverses rooted
    fragments and may reorder atoms; serial IDs carry correspondence.
    PDBQT cannot encode complete bonds, bond orders, formal charges, chemical
    states, interactions or arbitrary mechanics settings. Use conversion
    reports and strict mode to inspect representational losses. H5MSM 0.5
    does not persist the AutoDock labels and charges in MolecularMechanics.
    Named assignments emit a REMARK MOLSYSMT_PARTIAL_CHARGES JSON summary with
    the original producer versions, source coverage and total before rounding.
    Named typing emits a REMARK MOLSYSMT_ATOM_TYPES JSON summary with its
    scheme, rule version and original software. Reading PDBQT does not restore
    either complete mechanical assignment report.

    .. admonition:: Tutorial with more examples

       See :ref:`cookbook-native-pdbqt` for declared trees and conversion limits.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.pdbqt_adapter import write_payload
    from molsysmt._private.pdbqt_writer import serialize
    from molsysmt._private.variables import is_all
    from molsysmt.basic._index_validation import (
        validate_element_indices,
        validate_structure_indices,
    )

    from .extract import extract

    atoms = validate_element_indices(
        item, atom_indices, "atom", "atom_indices", "to_file_pdbqt"
    )
    frames = validate_structure_indices(item, structure_indices, "to_file_pdbqt")
    selected = item
    if not is_all(atoms) or not is_all(frames):
        selected = extract(item, atom_indices=atoms, structure_indices=frames)
    payload = serialize(
        selected, typing_scheme=typing_scheme, torsion_tree=torsion_tree
    )
    return write_payload(payload, output_filename)
