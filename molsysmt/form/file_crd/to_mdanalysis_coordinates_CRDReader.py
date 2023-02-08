from molsysmt._private.digestion import digest

@digest(form='file:crd')
def to_mdanalysis_coordinates_CRDReader(item, atom_indices='all', structure_indices='all'):

    from MDAnalysis.coordinates.CRD import CRDReader
    from ..mdanalysis_coordinates_CRDReader import extract as extract_mdanalysis_coordinates_CRDReader

    tmp_item = CRDReader(item)
    tmp_item = extract_mdanalysis_coordinates_CRDReader(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

