from molsysmt._private.exceptions import ArgumentError

def digest_in_place(in_place, caller=None):

    if isinstance(in_place, bool):
        return in_place
    else:
        raise ArgumentError('in_place', caller=caller, message=None)

