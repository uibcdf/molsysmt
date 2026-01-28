from molsysmt._private.digestion import digest

form = 'molsysviewer.MolSysView'


@digest(form=form)
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):

    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from ..molsysmt_MolSys.has_attribute import has_attribute as molsys_has_attribute

    tmp_item = to_molsysmt_MolSys(molecular_system, skip_digestion=True)
    if tmp_item is None:
        return False

    return molsys_has_attribute(tmp_item, attribute, include_none=include_none, skip_digestion=True)
