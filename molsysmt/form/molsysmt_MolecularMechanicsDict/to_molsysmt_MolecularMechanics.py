from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolecularMechanicsDict')
def to_molsysmt_MolecularMechanics(item):

    from molsysmt.native.molecular_mechanics import MolecularMechanics as molsysmt_MolecularMechanics

    tmp_item = molsysmt_MolecularMechanics(**item)

    return tmp_item

def to_molsysmt_MolecularMechanics(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_molsysmt_MolecularMechanics(item)
