from molsysmt._private.digestion import digest
from molsysmt.dependencies import requires

@digest(form='file:mmtf')
@requires('MDAnalysis')
def to_MDAnalysis_Universe(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from MDAnalysis import Universe

    from ..MDAnalysis_Universe import extract as extract_MDAnalysis_Universe

    tmp_item = Universe(item)
    tmp_item = extract_MDAnalysis_Universe(tmp_item, atom_indices=atom_indices,
                                           structure_indices=structure_indices, copy_if_all=False,
                                           skip_digestion=True
                                           )

    return tmp_item

