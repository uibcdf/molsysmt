from molsysmt._private.exceptions import ArgumentError

def digest_cosolutes(cosolutes, caller=None):

    if caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(cosolutes, (bool, int)):
            return cosolutes

    raise ArgumentError('cosolutes', value=cosolutes, caller=caller, message=None)

