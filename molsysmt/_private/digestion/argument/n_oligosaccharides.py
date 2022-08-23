from molsysmt._private.exceptions import ArgumentError

def digest_n_oligosaccharides(n_oligosaccharides, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_oligosaccharides, bool):
            return n_oligosaccharides

    raise ArgumentError('n_oligosaccharides', value=n_oligosaccharides, caller=caller, message=None)

