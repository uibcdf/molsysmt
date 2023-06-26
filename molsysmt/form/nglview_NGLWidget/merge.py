from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='nglview.NGLWidget')
def merge(items, atom_indices='all', structure_indices='all'):

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import merge

    if is_all(atom_indices):
        atom_indices = ['all' for ii in range(len(items))]

    if is_all(structure_indices):
        structure_indices = ['all' for ii in range(len(items))]

    items_molsysmt_MolSys = [to_molsysmt_MolSys(item) for item, atom in items]
    merged_items_molsysmt_MolSys = merge(items_molsysmt_MolSys)


    raise NotImplementedMethodError()

