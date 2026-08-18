from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw

@arg_digest(form='XYZ')
def to_cupy_ndarray(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from XYZ to cupy.ndarray.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    cupy.ndarray
        Resulting object in cupy.ndarray form.


    .. versionadded:: 1.0.0
    """
    import cupy as cp
    from molsysmt.form.XYZ.get_structural_attributes import get_coordinates_from_atom
    
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    val = puw.get_value(coordinates)
    unit = puw.get_unit(coordinates)
    
    gpu_val = cp.asarray(val)
    return puw.quantity(gpu_val, unit)
