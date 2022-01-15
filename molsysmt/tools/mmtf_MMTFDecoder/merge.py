def merge(item_1, item_2, check_form=True):

    if check_form:
        from molsysmt.tools.mmtf_MMTFDecoder import is_mmtf_MMTFDecoder
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_mmtf_MMTFDecoder(item_1):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')
        if not is_mmtf_MMTFDecoder(item_2):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    raise NotImplementedError

