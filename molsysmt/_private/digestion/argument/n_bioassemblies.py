from molsysmt._private.exceptions import ArgumentError

def digest_n_bioassemblies(n_bioassemblies, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_bioassemblies, bool):
            return n_bioassemblies

    raise ArgumentError('n_bioassemblies', value=n_bioassemblies, caller=caller, message=None)

