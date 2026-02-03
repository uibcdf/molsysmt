from ...exceptions import ArgumentError

def digest_to_html(to_html, caller=None):

    if isinstance(to_html, bool):
        return to_html

    raise ArgumentError('to_html', value=to_html, caller=caller, message=None)

