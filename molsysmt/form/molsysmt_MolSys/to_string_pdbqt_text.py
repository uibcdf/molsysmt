from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.MolSys")
def to_string_pdbqt_text(
    item,
    atom_indices="all",
    structure_indices="all",
    skip_digestion=False,
    *,
    typing_scheme=None,
    torsion_tree=None,
    return_atom_map=False,
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
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.
    typing_scheme : str or None, default=None
        Keyword-only explicit 'autodock4' declaration. None fails; labels are
        validated against chemical element symbols, without assigning them.
    torsion_tree : dict or None, default=None
        Keyword-only molsysmt.pdbqt-torsion-tree@1 dictionary bound to selected
        atom IDs and order. None writes a rigid receptor; a tree writes a ligand.
    return_atom_map : bool, default=False
        Return (text, completed atom-export map) when True, with actual written
        order, source indices/IDs, rooted traversal and charge-rounding evidence.

    Returns
    -------
    str or tuple
        Prefixed PDBQT text; optionally paired with a molsysmt.atom_export@1 dict.

    Raises
    ------
    FormatError
        For missing charges/types/coordinates, invalid field widths or tree,
        unsupported isotopes, nonnumeric atom IDs or multiple selected frames.

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

    .. admonition:: Tutorial with more examples

       See :ref:`cookbook-native-pdbqt` for declared trees and conversion limits.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.pdbqt_adapter import as_text, restore_export_axis
    from molsysmt._private.pdbqt_writer import serialize
    from molsysmt._private.variables import is_all
    from molsysmt.basic._index_validation import (
        validate_element_indices,
        validate_structure_indices,
    )

    from .extract import extract

    atoms = validate_element_indices(
        item, atom_indices, "atom", "atom_indices", "to_string_pdbqt_text"
    )
    frames = validate_structure_indices(item, structure_indices, "to_string_pdbqt_text")
    selected = item
    if not is_all(atoms) or not is_all(frames):
        selected = extract(item, atom_indices=atoms, structure_indices=frames)
    payload = serialize(
        selected,
        typing_scheme=typing_scheme,
        torsion_tree=torsion_tree,
        return_atom_map=return_atom_map,
    )
    if return_atom_map:
        payload, mapping = payload
        return as_text(payload), restore_export_axis(mapping, item, atoms, frames)
    return as_text(payload)
