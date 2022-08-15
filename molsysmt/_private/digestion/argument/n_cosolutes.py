from molsysmt._private.exceptions import ArgumentError

def digest_n_cosolutes(n_cosolutes, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_cosolutes, bool):
            return n_cosolutes

    raise ArgumentError('n_cosolutes', value=n_cosolutes, caller=caller, message=None)

