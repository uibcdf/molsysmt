from molsysmt._private.argdigest import arg_digest

from ._builder import build_molsys_builder_from_molsys_dict


@arg_digest(form='molsysmt.MolSysDict')
def to_molsysmt_MolSys(item, skip_digestion=False):
    """Converting MolSysDict to MolSys."""

    return build_molsys_builder_from_molsys_dict(item).build(skip_digestion=True)
