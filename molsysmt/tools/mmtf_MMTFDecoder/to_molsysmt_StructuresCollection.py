def to_molsysmt_StructuresCollection(item, atom_indices='all', structure_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.mmtf_MMTFDecoder.is_mmtf_MMTFDecoder import _checking_form
        _checking_form(item, check_form=check_form)

    from molsysmt.native.structures_collection import StructuresCollection
    from molsysmt.tools.mmtf_MMTFDecoder.get import get_step_from_system, get_time_from_system
    from molsysmt.tools.mmtf_MMTFDecoder.get import get_coordinates_from_atom, get_box_from_system

    step = get_step_from_system(item, structure_indices=structure_indices, check_form=False)
    time = get_time_from_system(item, structure_indices=structure_indices, check_form=False)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, check_form=False)
    box = get_box_from_system(item, structure_indices=structure_indices, check_form=False)

    tmp_item = StructuresCollection()
    tmp_item.append_structures(step=step, time=time, coordinates=coordinates, box=box)

    return tmp_item

