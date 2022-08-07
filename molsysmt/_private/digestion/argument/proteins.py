from molsysmt._private.exceptions import ArgumentError

def digest_proteins(proteins, caller=None):

    if caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(proteins, (bool, int)):
            return proteins

    raise ArgumentError('proteins', value=proteins, caller=caller, message=None)

