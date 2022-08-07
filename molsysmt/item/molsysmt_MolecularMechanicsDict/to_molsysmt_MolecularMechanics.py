from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolecularMechanicsDict')
def to_molsysmt_MolecularMechanics(item):

    from molsysmt.native.molecular_mechanics import MolecularMechanics as molsysmt_MolecularMechanics

    tmp_item = molsysmt_MolecularMechanics(**item)

    return tmp_item

