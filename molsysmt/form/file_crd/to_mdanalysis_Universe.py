from molsysmt._private.digestion import digest

@digest(form='file:crd')
def to_mdanalysis_Universe(item, atom_indices='all', structure_indices='all'):

    from MDAnalysis import Universe
    from ..mdanalysis_Universe import extract as extract_mdanalysis_Universe

    tmp_item = Universe(item)
    tmp_item = extract_mdanalysis_Universe(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

