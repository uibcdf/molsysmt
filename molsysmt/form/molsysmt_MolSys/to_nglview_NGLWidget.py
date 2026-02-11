from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form='molsysmt.MolSys')
def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.basic import extract
    try:
        from nglview import show_molsysmt
    except ImportError:
        from molsysmt.thirds.nglview.molsysmt_trajectory import show_molsysmt

    if not (is_all(atom_indices) and is_all(structure_indices)):
        tmp_item = extract(item, selection=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    else:
        tmp_item = item

    tmp_item = show_molsysmt(tmp_item, skip_digestion=True)

    return tmp_item
