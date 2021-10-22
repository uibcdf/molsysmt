def from_mmtf_MMTFDecoder(item, atom_indices='all', frame_indices='all', bioassembly_index=0, bioassembly_name=None):


    from molsysmt.native.io.dataframe.classes import from_mmtf_MMTFDecoder as molsysmt_dataframe_from_mmtf_MMTFDecoder
    from molsysmt.native.io.topology import from_molsysmt_DataFrame as molsysmt_topology_from_molsysmt_DataFrame
    from numpy import reshape, sum

    dataframe = molsysmt_dataframe_from_mmtf_MMTFDecoder(item, atom_indices='all',
            frame_indices='all', bioassembly_index=bioassembly_index,
            bioassembly_name=bioassembly_name)

    tmp_item = molsysmt_topology_from_molsysmt_DataFrame(dataframe)

    # End

    if atom_indices is not 'all':
        tmp_item = tmp_item.extract(atom_indices=atom_indices)

    return tmp_item

