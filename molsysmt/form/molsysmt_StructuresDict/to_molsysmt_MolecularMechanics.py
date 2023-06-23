from molsysmt._private.digestion import digest

@digest(form='molsysmt.StructuresDict')
def to_molsysmt_MolecularMechanics(item, atom_indices='all', structure_indices='all'):

    from molsysmt.native.molecular_mechanics import MolecularMechanics

    tmp_item = MolecularMechanics()

    return tmp_item

