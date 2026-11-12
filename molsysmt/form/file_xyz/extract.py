from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="file:xyz")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    copy_if_all=True,
    skip_digestion=False,
):
    """
    Extracting a subset of elements or structures from form file:xyz.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_filename : str or pathlib.Path, default=None
        Destination for an independent file. None creates a session-owned
        temporary copy for whole-file extraction; supported subset writers
        follow the same independent-output policy.
    copy_if_all : bool, default=True
        Whether to copy a complete selection. False permits returning the
        source when no distinct destination is requested. A distinct explicit
        destination is honored regardless of this flag.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:xyz
        Resulting object in file:xyz form.


    Raises
    ------
    ArgumentError
        If a requested copy destination aliases the source or names a directory.


    .. versionadded:: 1.0.0
    """

    if is_all(atom_indices) and is_all(structure_indices):
        if not copy_if_all and (
            output_filename is None or str(output_filename) == str(item)
        ):
            return item
        from molsysmt._private.files_and_directories import copy_file

        return copy_file(item, output_filename, caller="molsysmt.form.file_xyz.extract")

    else:
        from molsysmt._private.files_and_directories import file_copy_destination

        with file_copy_destination(
            item, output_filename, caller="molsysmt.form.file_xyz.extract"
        ) as destination:
            from .get_structural_attributes import _read_xyz

            coords = _read_xyz(item)

            if not is_all(structure_indices):
                coords = coords[structure_indices, :, :]
            if not is_all(atom_indices):
                coords = coords[:, atom_indices, :]

            n_structures, n_atoms, _ = coords.shape

            with open(destination, "w") as f:
                f.write(f"{n_structures} {n_atoms}\n")
                for s in range(n_structures):
                    for a in range(n_atoms):
                        x, y, z = coords[s, a]
                        f.write(f"{x:.8f} {y:.8f} {z:.8f}\n")

            tmp_item = destination

    return tmp_item
