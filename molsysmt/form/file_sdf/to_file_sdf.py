from pathlib import Path

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:sdf")
def to_file_sdf(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    ctfile_version="V2000",
    discard_properties=False,
    skip_digestion=False,
):
    """Copying an SDF file or serializing an explicitly selected native subset.

    Parameters
    ----------
    item : str or pathlib.Path
        Single-record SDF source file.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include; all indices preserve source bytes.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include; only index zero exists.
    output_filename : str or pathlib.Path, default=None
        Destination path; None returns the unchanged source for an identity route.
    ctfile_version : {'V2000', 'V3000'}, default='V2000'
        Syntax for a projected subset; an identity copy retains the source syntax.
    discard_properties : bool, default=False
        Explicitly authorize dropping SD properties when projecting a subset.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    str or pathlib.Path
        Source or destination path according to the requested operation.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.ctfile import _fail, read_sdf
    from molsysmt._private.variables import is_all
    from molsysmt.form.molsysmt_MolSys.to_file_sdf import to_file_sdf as native_write

    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    if is_all(atom_indices) and is_all(structure_indices):
        read_sdf(item)
        if output_filename is None:
            return item
        payload = Path(item).read_bytes()
        Path(output_filename).write_bytes(payload)
        return output_filename
    if output_filename is None:
        _fail("Subset SDF serialization requires an output_filename.")
    native = to_molsysmt_MolSys(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        discard_properties=discard_properties,
        skip_digestion=True,
    )
    return native_write(
        native,
        output_filename=output_filename,
        ctfile_version=ctfile_version,
        skip_digestion=True,
    )
