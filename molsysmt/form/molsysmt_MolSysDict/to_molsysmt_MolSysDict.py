from molsysmt._private.arg_digestion import arg_digest


@arg_digest(form='molsysmt.MolSysDict')
def to_molsysmt_MolSysDict(item, skip_digestion=False):
    """Copying MolSysDict."""
    return item.copy()
