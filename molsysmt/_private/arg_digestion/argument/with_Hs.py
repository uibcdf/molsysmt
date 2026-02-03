from molsysmt._private.exceptions import ArgumentError

def digest_with_Hs(with_Hs, caller=None):

    if isinstance(with_Hs, bool):
        return with_Hs

    raise ArgumentError('with_Hs', value=with_Hs, caller=caller, message=None)

