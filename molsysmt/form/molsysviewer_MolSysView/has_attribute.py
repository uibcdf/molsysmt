from molsysmt._private.arg_digestion import arg_digest

form = 'molsysviewer.MolSysView'


@arg_digest(form=form)
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):

    from molsysmt.form.molsysmt_MolSys.to_molsysmt_MolSys import to_molsysmt_MolSys
    from ..molsysmt_MolSys.has_attribute import has_attribute as molsys_has_attribute

    tmp_item = to_molsysmt_MolSys(molecular_system, skip_digestion=True)
    if tmp_item is None:
        return False

    return molsys_has_attribute(tmp_item, attribute, include_none=include_none, skip_digestion=True)
