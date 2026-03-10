from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.H5MSMFileHandler')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):

    from . import attributes

    output = attributes[attribute]

    if not include_none:

        if attribute == 'b_factor':
            if 'b_factor' not in molecular_system.file['structures']:
                output = False
            elif molecular_system.file['structures']['b_factor'].shape[0] == 0:
                output = False

    return output
