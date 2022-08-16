from molsysmt._private.exceptions import ArgumentError

def digest_oligosaccharides(oligosaccharides, caller=None):

    if caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(oligosaccharides, (bool, int)):
            return oligosaccharides
    elif caller=='molsysmt.basic.contains.contains':
        if isinstance(oligosaccharides, (bool, int)):
            return oligosaccharides
        elif oligosaccharides is None:
            return None


    raise ArgumentError('oligosaccharides', value=oligosaccharides, caller=caller, message=None)

