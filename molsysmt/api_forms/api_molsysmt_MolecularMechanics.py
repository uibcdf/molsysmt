def to_MolecularMechanicsDict(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolecularMechanics import \
        to_molsysmt_MolecularMechanicsDict as molsysmt_MolecularMechanics_to_molsysmt_MolecularMechanicsDict

    return molsysmt_MolecularMechanics_to_molsysmt_MolecularMechanicsDict(item)
