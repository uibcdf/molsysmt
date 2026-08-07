from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.MolSysBuilder")
def to_molsysmt_MolSysBuilder(item, skip_digestion=False):
    return item.copy()
