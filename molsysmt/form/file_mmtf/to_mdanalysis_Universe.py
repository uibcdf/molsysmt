from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import LibraryNotFoundError

@digest(form='file:mmtf')
def to_mdanalysis_Universe(item, atom_indices='all', structure_indices='all', digest=True):

    try:
        from MDAnalysis import Universe
    except:
        raise LibraryNotFoundError('MDAnalysis')

    from ..mdanalysis_Universe import extract as extract_mdanalysis_Universe

    tmp_item = Universe(item)
    tmp_item = extract_mdanalysis_Universe(tmp_item, atom_indices=atom_indices,
                                           structure_indices=structure_indices, copy_if_all=False,
                                           digest=False)

    return tmp_item

