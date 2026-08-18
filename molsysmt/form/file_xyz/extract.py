from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import numpy as np

@arg_digest(form='file:xyz')
def extract(item, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True,
            skip_digestion=False):
    """
    Extracting a subset of elements or structures from form file:xyz.

    Parameters
    ----------
    item : file:xyz
        Source item in file:xyz form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    output_filename : str or pathlib.Path
        Output file path for serialization.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:xyz
        Resulting object in file:xyz form.

    .. versionadded:: 1.0.0
    """

    if output_filename is None:
        output_filename = item

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all or (output_filename != item):

            from shutil import copy as copy_file
            copy_file(item, output_filename)
            tmp_item = output_filename

        else:

            tmp_item = item

    else:

        from .get_structural_attributes import _read_xyz

        coords = _read_xyz(item)

        if not is_all(structure_indices):
            coords = coords[structure_indices, :, :]
        if not is_all(atom_indices):
            coords = coords[:, atom_indices, :]

        n_structures, n_atoms, _ = coords.shape

        with open(output_filename, 'w') as f:
            f.write(f"{n_structures} {n_atoms}\n")
            for s in range(n_structures):
                for a in range(n_atoms):
                    x, y, z = coords[s, a]
                    f.write(f"{x:.8f} {y:.8f} {z:.8f}\n")

        tmp_item = output_filename

    return tmp_item
