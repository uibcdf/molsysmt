from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import LibraryNotFoundError

@digest(form='file:mmtf')
def to_MDAnalysis_Universe(item, atom_indices='all', structure_indices='all'):

    try:
        from MDAnalysis import Universe
    except:
        raise LibraryNotFoundError('MDAnalysis')

    from ..MDAnalysis_Universe import extract as extract_MDAnalysis_Universe

    tmp_item = Universe(item)
    tmp_item = extract_MDAnalysis_Universe(tmp_item, atom_indices=atom_indices,
                                           structure_indices=structure_indices, copy_if_all=False,
                                           )

    return tmp_item

def _to_MDAnalysis_Universe(item, atom_indices='all', structure_indices='all'):

    return to_MDAnalysis_Universe(item, atom_indices=atom_indices, structure_indices=structure_indices)
