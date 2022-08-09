from molsysmt._private.exceptions import ArgumentError

def digest_cosolutes(cosolutes, caller=None):

    if caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(cosolutes, (bool, int)):
            return cosolutes
    if caller=='molsysmt.basic.contains.contains':
        if isinstance(cosolutes, (bool, int)):
            return cosolutes
        elif cosolutes is None:
            return None

    raise ArgumentError('cosolutes', value=cosolutes, caller=caller, message=None)

