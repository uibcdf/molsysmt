def to_mdanalysis_coordinates_CRDReader(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from MDAnalysis.coordinates.CRD import CRDReader

    tmp_item = CRDReader(item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

