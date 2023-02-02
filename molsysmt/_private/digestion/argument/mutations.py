from molsysmt._private.exceptions import ArgumentError

def digest_mutations(mutations, caller=None):


    if caller == 'molsysmt.build.mutate.mutate':

        if isinstance(mutations, dict):
            return mutations
        elif isinstance(mutations, str):
            return [mutations]
        elif isinstance(mutations, (list, tuple)):
            return mutations

    raise ArgumentError('mutations', value=mutations, caller=caller, message=None)
