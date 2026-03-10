from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:h5msm')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=True):

    from . import attributes
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    output = attributes[attribute]

    if not include_none:
        if attribute == 'b_factor':
            tmp_item = to_molsysmt_H5MSMFileHandler(molecular_system, skip_digestion=True)
            output = ('b_factor' in tmp_item.file['structures']) and (tmp_item.file['structures']['b_factor'].shape[0] > 0)
            tmp_item.close()

    return output
