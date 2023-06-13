from molsysmt._private.exceptions import ArgumentError

def digest_n_oligosaccharides(n_oligosaccharides, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_oligosaccharides, bool):
            return n_oligosaccharides
    elif caller=='molsysmt.basic.contains.contains':
        if isinstance(n_molecules, (bool, int)):
            return n_molecules


    raise ArgumentError('n_oligosaccharides', value=n_oligosaccharides, caller=caller, message=None)

