from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_mdanalysis_Universe(item, atom_indices='all', structure_indices='all'):

    try:
        from MDAnalysis import Universe
    except:
        raise LibraryNotFound('MDAnalysis')

    from ..mdanalysis_Universe import extract

    tmp_item = Universe(item)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False)

    return tmp_item

