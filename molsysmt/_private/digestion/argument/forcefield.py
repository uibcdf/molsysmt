from molsysmt._private.exceptions import ArgumentError

def digest_forcefield(forcefield, caller=None):

    if isinstance(forcefield, str):
        return forcefield

    raise ArgumentError('forcefield', value=forcefield, caller=caller, message=None)

