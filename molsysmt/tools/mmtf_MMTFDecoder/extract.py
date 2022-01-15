def extract(item, atom_indices='all', frame_indices='all', copy_if_all=True, check_form=True):

    if check_form:
        from molsysmt.tools.mmtf_MMTFDecoder import is_mmtf_MMTFDecoder
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    if (atom_indices is 'all') and (frame_indices is 'all'):
        from copy import deepcopy
        tmp_item = deepcopy(item)
    else:
        raise NotImplementedError()

    return tmp_item

