from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='mdtraj.Topology')
def to_parmed_GromacsTopologyFile(item, atom_indices='all', skip_digestion=False):

    from molsysmt.form.parmed_Structure import to_parmed_Structure
    from molsysmt.form.parmed_Structure import to_parmed_GromacsTopologyFile as parmed_Structure_to_parmed_GromacsTopologyFile

    tmp_item = to_parmed_Structure(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = parmed_Structure_to_parmed_GromacsTopologyFile(tmp_item, skip_digestion=True)

    return tmp_item

