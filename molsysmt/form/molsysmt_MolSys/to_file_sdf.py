from pathlib import Path

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.MolSys")
def to_file_sdf(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    ctfile_version="V2000",
    skip_digestion=False,
):
    """Writing one native molecular structure as an explicit SDF record.

    Parameters
    ----------
    item : molsysmt.MolSys
        Native system with a complete graph and explicit formal charges/radicals.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include in native MolSys extraction order.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include; exactly one must be selected.
    output_filename : str or pathlib.Path, default=None
        Destination SDF path. It is opened only after complete validation.
    ctfile_version : {'V2000', 'V3000'}, default='V2000'
        Explicit connection-table syntax. V2000 supports at most 999 atoms/bonds.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    str or pathlib.Path
        Destination path, containing coordinates explicitly expressed in angstroms.

    Raises
    ------
    FormatError
        For missing chemistry, multiple frames/states, or unsupported stereo/bonds.

    Notes
    -----
    Atom and bond serials are assigned by output order. SDF does not retain
    arbitrary native IDs, hierarchy, mechanics, interactions or SD properties.
    Coordinates are converted explicitly to angstroms, regardless of unit policy.
    Atom aromaticity must be recoverable from the supplied explicit aromatic
    bond types; unencodable or contradictory assignments fail explicitly.

    .. admonition:: Tutorial with more examples

       See :ref:`cookbook-native-sdf` for selection and information-loss policies.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.ctfile import _fail, write_sdf
    from molsysmt._private.variables import is_all
    from molsysmt.basic._index_validation import validate_structure_indices
    from molsysmt.form.file_sdf._native import from_native

    from .extract import extract

    if output_filename is None:
        _fail("An output_filename is required for SDF serialization.")
    structure_indices = validate_structure_indices(
        item, structure_indices, "to_file_sdf"
    )
    selected = item
    if not is_all(atom_indices) or not is_all(structure_indices):
        selected = extract(
            item,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            skip_digestion=True,
        )
    payload = write_sdf(from_native(selected, ctfile_version))
    try:
        encoded = payload.encode("utf-8")
    except UnicodeEncodeError:
        _fail("SDF text must be encodable as UTF-8.")
    Path(output_filename).write_bytes(encoded)
    return output_filename
