from molsysmt._private.argdigest import arg_digest

@arg_digest(form='parmed.GromacsTopologyFile')
def to_parmed_Structure(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    from molsysmt.form.parmed_Structure.extract import extract as parmed_Structure_extract

    return parmed_Structure_extract(item, atom_indices=atom_indices,
                                    structure_indices=structure_indices,
                                    copy_if_all=copy_if_all, skip_digestion=True)
