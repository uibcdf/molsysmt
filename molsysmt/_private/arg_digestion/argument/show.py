from molsysmt._private.smonitor import ArgumentError


def digest_show(show, caller=None):

    if isinstance(show, bool):
        return show

    raise ArgumentError('show', value=show, caller=caller, message=None)
