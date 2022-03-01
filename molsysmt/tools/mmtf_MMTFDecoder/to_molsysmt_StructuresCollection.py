def to_molsysmt_StructuresCollection(item, atom_indices='all', structure_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.mmtf_MMTFDecoder.is_mmtf_MMTFDecoder import _checking_form
        _checking_form(item, check_form=check_form)

    from molsysmt.native.structures_collection import StructuresCollection
    from molsysmt.tools.mmtf_MMTFDecoder.get import get_frame_from_atom

    tmp_item = StructuresCollection()
    step, time, coordinates, box = get_frame_from_atom(item, indices=atom_indices, structure_indices=structure_indices, check_form=False)
    tmp_item.append_structures(step=step, time=time, coordinates=coordinates, box=box)

    return tmp_item

