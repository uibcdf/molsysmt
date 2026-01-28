from molsysmt._private.digestion import digest

form = 'molsysviewer.MolSysView'


@digest(form=form)
def extract(item, selection='all', structure_indices='all', syntax='MolSysMT', skip_digestion=False):

    from molsysmt.basic import extract as molsys_extract, convert
    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    if tmp_item is None:
        return None

    tmp_item = molsys_extract(tmp_item, selection=selection, structure_indices=structure_indices,
                              syntax=syntax, skip_digestion=True)
    return convert(tmp_item, to_form='molsysviewer.MolSysView', skip_digestion=True)
