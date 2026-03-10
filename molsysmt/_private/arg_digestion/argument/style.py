from molsysmt._private.smonitor import ArgumentError


def digest_style(style, caller=None):

    if caller == 'molsysmt.structure.show_contacts.show_contacts':
        if style in ['plotly', 'matplotlib']:
            return style

    raise ArgumentError('style', value=style, caller=caller, message=None)
