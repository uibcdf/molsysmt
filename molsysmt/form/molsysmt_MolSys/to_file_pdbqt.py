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
    return_atom_map=False,
    output_presentation=None,
    remarks=None,
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
    return_atom_map : bool, default=False
        Return (destination, completed atom-export map) when True. The map records
        actual written order, source indices/IDs, rooted traversal and charge rounding.

    output_presentation : dict or None, default=None
        Keyword-only output fields, without changing source IDs or hierarchy.
        Keys: atom_serials ('preserve', 'consecutive', or explicit serials),
        atom_names, group_names, group_ids, chain_ids, occupancy and b_factor.
        Scalars broadcast; vectors follow the original input atom axis, before
        selection. Consecutive serials follow actual tree traversal. B factors
        require squared-length quantities; occupancy is dimensionless. None
        clears optional occupancy/B-factor fields. Omitted keys preserve data.
    remarks : list, tuple, numpy.ndarray or None, default=None
        Keyword-only complete printable ASCII 'REMARK ...' lines. Maximum 4096
        characters per line and 64 KiB total, including line endings. Newlines,
        control characters and the reserved MOLSYSMT_ namespace are rejected.
        Provider provenance remains separate. The export hash covers final bytes.

    Returns
    -------
    str, pathlib.Path or tuple
        Destination path; optionally paired with a molsysmt.atom_export@1 dict.

    Raises
    ------
    FormatError
        For missing charges/types/coordinates, invalid field widths or tree,
        unsupported isotopes, invalid serials or multiple selected structures.
    StructuralInconsistencyError
        For named charge/type assignments that no longer match bound chemistry,
        ordered values, associated chemical state or requested typing scheme.

    Notes
    -----
    Coordinates are explicitly converted to angstroms, independent of the
    session unit policy; charges are native values in elementary charge.
    Every input hydrogen is retained. No hydrogen merging, charge aggregation,
    typing, rotatable-bond perception or molecular preparation is performed.
    By default, serials preserve unique canonical positive integer source IDs.
    Explicit serial presentation also accepts arbitrary source labels. Tree
    serialization may reorder atoms; export maps retain original source IDs
    and indices separately from written serials and names. Group/chain output
    labels do not create native membership or certify chemical preparation.
    Caller remarks precede atom/tree records, after provider provenance; maps
    and SHA-256 are completed only after forming the final UTF-8 payload.
    PDBQT cannot encode complete bonds, bond orders, formal charges, chemical
    states, interactions or arbitrary mechanics settings. Use conversion
    reports and strict mode to inspect representational losses. H5MSM 0.5
    does not persist the AutoDock labels and charges in MolecularMechanics.
    Named assignments emit a REMARK MOLSYSMT_PARTIAL_CHARGES JSON summary with
    the original producer versions, source coverage and total before rounding.
    Named typing emits a REMARK MOLSYSMT_ATOM_TYPES JSON summary with its
    scheme, rule version and original software. Reading PDBQT does not restore
    either complete mechanical assignment report.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.native import MolSys
    >>> molsys = MolSys(n_atoms=1)
    >>> msm.set(molsys, atom_id=['source-C'], atom_name=['C'], atom_type=['C'])
    >>> molsys.structures.coordinates = msm.pyunitwizard.quantity([[[0, 0, 0]]], 'nm')
    >>> molsys.molecular_mechanics.atom_ff_type = ['C']
    >>> molsys.molecular_mechanics.partial_charge = [0.0]
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory() as directory:
    ...     destination, atom_map = to_file_pdbqt(molsys,
    ...         output_filename=Path(directory) / 'carbon.pdbqt', typing_scheme='autodock4',
    ...         output_presentation={'atom_serials': 'consecutive'}, return_atom_map=True)
    ...     print(atom_map['source_atom_ids'].tolist(), Path(destination).is_file())
    ['source-C'] True

    .. admonition:: Tutorial with more examples

       See :ref:`cookbook-native-pdbqt` for declared trees and conversion limits.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.pdbqt_adapter import restore_export_axis, write_payload
    from molsysmt._private.pdbqt_presentation import select as select_presentation
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
    output_presentation = select_presentation(
        output_presentation,
        None if item.topology is None else item.topology.n_atoms,
        atoms,
    )
    selected = item
    if not is_all(atoms) or not is_all(frames):
        selected = extract(item, atom_indices=atoms, structure_indices=frames)
    payload = serialize(
        selected,
        typing_scheme=typing_scheme,
        torsion_tree=torsion_tree,
        return_atom_map=return_atom_map,
        output_presentation=output_presentation,
        remarks=remarks,
    )
    if return_atom_map:
        payload, mapping = payload
        mapping = restore_export_axis(mapping, item, atoms, frames)
        return write_payload(payload, output_filename), mapping
    return write_payload(payload, output_filename)
