from molsysmt._private.arg_digestion import arg_digest
@arg_digest(form='file:psf')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    return to_molsysmt_MolSys(
        item, atom_indices=atom_indices, skip_digestion=True
    ).topology
