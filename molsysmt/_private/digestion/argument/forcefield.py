from molsysmt._private.exceptions import ArgumentError

def digest_forcefield(forcefield, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(forcefield, bool):
            return forcefield
    elif caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return forcefield
    elif isinstance(forcefield, str):
        return forcefield

    raise ArgumentError('forcefield', value=forcefield, caller=caller, message=None)

