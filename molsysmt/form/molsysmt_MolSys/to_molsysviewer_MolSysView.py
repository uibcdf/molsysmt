from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all


@digest(form='molsysmt.MolSys')
def to_molsysviewer_MolSysView(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysviewer import MolSysView
    from molsysmt.basic import extract

    if not (is_all(atom_indices) and is_all(structure_indices)):
        tmp_item = extract(item, selection=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    else:
        tmp_item = item

    view = MolSysView()
    view.load(tmp_item, selection='all', structure_indices='all', syntax='MolSysMT')

    return view
