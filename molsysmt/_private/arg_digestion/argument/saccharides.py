from molsysmt._private.exceptions import ArgumentError

def digest_saccharides(saccharides, caller=None):

    if caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(saccharides, (bool, int)):
            return saccharides
    elif caller=='molsysmt.basic.contains.contains':
        if isinstance(saccharides, (bool, int)):
            return saccharides
        elif saccharides is None:
            return None


    raise ArgumentError('saccharides', value=saccharides, caller=caller, message=None)

