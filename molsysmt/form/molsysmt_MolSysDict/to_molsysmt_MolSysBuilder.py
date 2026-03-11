from molsysmt._private.arg_digestion import arg_digest

from ._builder import build_molsys_builder_from_molsys_dict


@arg_digest(form="molsysmt.MolSysDict")
def to_molsysmt_MolSysBuilder(item, skip_digestion=False):
    """Converting MolSysDict to MolSysBuilder."""

    return build_molsys_builder_from_molsys_dict(item)
