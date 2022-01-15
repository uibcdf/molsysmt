def add(to_item, item, check_form=True):

    if check_form:
        from molsysmt.tools.mmtf_MMTFDecoder import is_mmtf_MMTFDecoder
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')
        if not is_mmtf_MMTFDecoder(to_item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    raise NotImplementedError

