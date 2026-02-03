from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.MoleculeMechanics')
def to_molsysmt_MolecularMechanics(item, copy_if_all=True, skip_digestion=False):

    from .extract import extract

    return extract(item, copy_if_all=copy_if_all, skip_digestion=True)

