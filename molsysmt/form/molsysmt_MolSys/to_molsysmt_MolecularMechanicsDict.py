from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def to_molsysmt_MolecularMechanicsDict(item, atom_indices='all'):

    from ..molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanicsDict as molsysmt_MolecularMechanics_to_MolecularMechanicsDict

    tmp_item = molsysmt_MolecularMechanics_to_MolecularMechanicsDict(item.molecular_mechanics, atom_indices='all')

    return tmp_item


