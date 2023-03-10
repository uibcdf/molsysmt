from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolecularMechanics')
def to_molsysmt_MolecularMechanicsDict(item):

    tmp_item = item.to_dict()

    return tmp_item
