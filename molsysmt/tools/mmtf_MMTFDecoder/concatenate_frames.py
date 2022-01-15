def concatenate_frames(item, step=None, time=None, coordinates=None, box=None, check_form=True):

    if check_form:
        from molsysmt.tools.mmtf_MMTFDecoder import is_mmtf_MMTFDecoder
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    raise NotImplementedError

