from molsysmt._private.arg_digestion import arg_digest


@arg_digest(form="molsysmt.MolSys")
def to_molsysmt_MolSysBuilder(item, atom_indices="all", structure_indices="all", skip_digestion=False):

    from molsysmt.native import MolSysBuilder

    molsys = item.extract(
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        copy_if_all=True,
        skip_digestion=True,
    )

    return MolSysBuilder(molsys, skip_digestion=True)
