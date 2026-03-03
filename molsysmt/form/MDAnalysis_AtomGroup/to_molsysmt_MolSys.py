from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='MDAnalysis.AtomGroup')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.form.MDAnalysis_Universe.to_molsysmt_MolSys import to_molsysmt_MolSys as MDAnalysis_Universe_to_molsysmt_MolSys
    from molsysmt._private.variables import is_all

    indices = item.indices

    if not is_all(atom_indices):
        indices = indices[atom_indices]

    tmp_item = MDAnalysis_Universe_to_molsysmt_MolSys(item.universe, atom_indices=indices, 
                                                      structure_indices=structure_indices, skip_digestion=True)

    return tmp_item
