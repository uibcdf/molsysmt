from molsysmt._private.arg_digestion import arg_digest

form = 'molsysviewer.MolSysView'


@arg_digest(form=form)
def copy(item, skip_digestion=False):

    from molsysmt.basic import copy as molsys_copy, convert
    from molsysmt.form.molsysmt_MolSys.to_molsysmt_MolSys import to_molsysmt_MolSys

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    if tmp_item is None:
        return None

    tmp_item = molsys_copy(tmp_item, skip_digestion=True)
    return convert(tmp_item, to_form='molsysviewer.MolSysView', skip_digestion=True)
