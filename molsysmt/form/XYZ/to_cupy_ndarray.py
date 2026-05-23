from molsysmt._private.arg_digestion import arg_digest
from molsysmt import pyunitwizard as puw

@arg_digest(form='XYZ')
def to_cupy_ndarray(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    import cupy as cp
    from molsysmt.form.XYZ.get_structural_attributes import get_coordinates_from_atom
    
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    val = puw.get_value(coordinates)
    unit = puw.get_unit(coordinates)
    
    gpu_val = cp.asarray(val)
    return puw.quantity(gpu_val, unit)
