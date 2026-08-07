from molsysmt._private.argdigest import arg_digest

@arg_digest(form='MDAnalysis.AtomGroup')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.form.MDAnalysis_Universe.to_molsysmt_Topology import to_molsysmt_Topology as MDAnalysis_Universe_to_molsysmt_Topology
    from molsysmt._private.variables import is_all

    # Get the indices of the atoms in the AtomGroup relative to the Universe
    indices = item.indices

    if not is_all(atom_indices):
        indices = indices[atom_indices]

    tmp_item = MDAnalysis_Universe_to_molsysmt_Topology(item.universe, atom_indices=indices, skip_digestion=True)

    return tmp_item
