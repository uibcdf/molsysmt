from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.MolSysBuilder")
def to_molsysmt_MolSys(item, atom_indices="all", structure_indices="all", copy_if_all=True, skip_digestion=False):

    if atom_indices != "all" or structure_indices != "all":
        return item.build(skip_digestion=True).extract(
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            copy_if_all=copy_if_all,
            skip_digestion=True,
        )

    return item.build(skip_digestion=True)
