from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import types

form = 'file:xyz'


def _read_xyz(item):
    """Read the full coordinate array from an xyz file.

    Returns
    -------
    coords : np.ndarray, shape (n_structures, n_atoms, 3), dtype float64
        Coordinates in nm.
    """
    with open(item, 'r') as f:
        header = f.readline().strip().split()
        n_structures, n_atoms = int(header[0]), int(header[1])
        data = []
        for _ in range(n_structures * n_atoms):
            row = f.readline().strip().split()
            data.append([float(row[0]), float(row[1]), float(row[2])])
    coords = np.array(data, dtype=np.float64).reshape(n_structures, n_atoms, 3)
    return coords


def _read_header(item):
    """Read only n_structures and n_atoms from the file header."""
    with open(item, 'r') as f:
        header = f.readline().strip().split()
    return int(header[0]), int(header[1])


@arg_digest(form=form)
def get_n_atoms_from_system(item, structure_indices='all', skip_digestion=False):

    _, n_atoms = _read_header(item)
    return n_atoms


@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    n_structures, _ = _read_header(item)
    if not is_all(structure_indices):
        return len(structure_indices)
    return n_structures


@arg_digest(form=form)
def get_structure_index_from_system(
    item, structure_indices='all', skip_digestion=False
):

    n_structures, _ = _read_header(item)
    output = np.arange(n_structures, dtype=int)
    if not is_all(structure_indices):
        output = output[structure_indices]
    return output.tolist()


@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    _, n_atoms = _read_header(item)
    output = np.arange(n_atoms)
    if not is_all(indices):
        output = output[indices]
    return output.tolist()


@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    coords = _read_xyz(item)

    if not is_all(structure_indices):
        coords = coords[structure_indices, :, :]

    if not is_all(indices):
        coords = coords[:, indices, :]

    output = coords * puw.unit('nm')
    output = puw.standardize(output)

    return output


@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):

    coords = _read_xyz(item)

    if not is_all(structure_indices):
        coords = coords[structure_indices, :, :]

    output = coords * puw.unit('nm')
    output = puw.standardize(output)

    return output


# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
