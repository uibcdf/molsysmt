from molsysmt._private.arg_digestion import arg_digest
from molsysmt import pyunitwizard as puw

@arg_digest(form='cupy_ndarray')
def to_XYZ(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    import cupy as cp
    val = puw.get_value(item)
    unit = puw.get_unit(item)
    
    cpu_val = cp.asnumpy(val)
    from molsysmt.form.XYZ.get_structural_attributes import get_coordinates_from_atom
    cpu_qty = puw.quantity(cpu_val, unit)
    return get_coordinates_from_atom(cpu_qty, indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
