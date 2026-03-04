from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form='molsysviewer.MolSysView')
def to_molsysviewer_MolSysView(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysviewer import MolSysView
    from molsysmt.basic import extract
    from molsysmt.form.molsysmt_MolSys.to_molsysmt_MolSys import to_molsysmt_MolSys

    if is_all(atom_indices) and is_all(structure_indices):
        return item

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    if tmp_item is None:
        return None

    tmp_item = extract(tmp_item, selection=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    view = MolSysView()
    view.load(tmp_item, selection='all', structure_indices='all', syntax='MolSysMT')

    return view
