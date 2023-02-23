from molsysmt._private.exceptions import ArgumentError

def digest_forcefield(forcefield, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(forcefield, bool):
            return forcefield

    if isinstance(forcefield, str):
        return forcefield

    raise ArgumentError('forcefield', value=forcefield, caller=caller, message=None)

