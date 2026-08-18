from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw

@arg_digest(form='cupy_ndarray')
def to_XYZ(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from cupy_ndarray to XYZ.


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
    XYZ
        Resulting object in XYZ form.


    .. versionadded:: 1.0.0
    """
    import cupy as cp
    val = puw.get_value(item)
    unit = puw.get_unit(item)
    
    cpu_val = cp.asnumpy(val)
    from molsysmt.form.XYZ.get_structural_attributes import get_coordinates_from_atom
    cpu_qty = puw.quantity(cpu_val, unit)
    return get_coordinates_from_atom(cpu_qty, indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
