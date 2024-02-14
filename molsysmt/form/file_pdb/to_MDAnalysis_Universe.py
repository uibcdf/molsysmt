from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_MDAnalysis_Universe(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    try:
        from MDAnalysis import Universe
    except:
        raise LibraryNotFound('MDAnalysis')

    from ..MDAnalysis_Universe import extract

    tmp_item = Universe(item)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, skip_digestion=True)

    return tmp_item

