def is_mmtf_MMTFDecoder(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'mmtf.api.mmtf_reader.MMTFDecoder')

    return output

