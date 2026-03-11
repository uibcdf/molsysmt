from molsysmt._private.arg_digestion import arg_digest


@arg_digest(form='file:molsys_yaml')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    from .to_molsysmt_MolSysDict import to_molsysmt_MolSysDict
    from molsysmt.form.molsysmt_MolSysDict.has_attribute import has_attribute as dict_has_attribute

    item = to_molsysmt_MolSysDict(molecular_system, skip_digestion=True)
    return dict_has_attribute(item, attribute=attribute, include_none=include_none, skip_digestion=True)
