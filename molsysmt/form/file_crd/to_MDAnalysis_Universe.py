from molsysmt._private.digestion import digest

@digest(form='file:crd')
def to_MDAnalysis_Universe(item, atom_indices='all', structure_indices='all'):

    from MDAnalysis import Universe
    from ..MDAnalysis_Universe import extract as extract_MDAnalysis_Universe

    tmp_item = Universe(item)
    tmp_item = extract_MDAnalysis_Universe(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

