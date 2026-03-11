from molsysmt._private.arg_digestion import arg_digest


@arg_digest(form='file:molsys_yaml')
def to_molsysmt_MolSys(item, skip_digestion=False):
    """Converting a YAML molecular system file into MolSys."""

    from .to_molsysmt_MolSysDict import to_molsysmt_MolSysDict
    from molsysmt.form.molsysmt_MolSysDict.to_molsysmt_MolSys import to_molsysmt_MolSys as dict_to_molsys

    tmp_item = to_molsysmt_MolSysDict(item, skip_digestion=True)
    return dict_to_molsys(tmp_item, skip_digestion=True)
