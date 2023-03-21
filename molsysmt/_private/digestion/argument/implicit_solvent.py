from molsysmt._private.exceptions import ArgumentError

def digest_implicit_solvent(implicit_solvent, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(implicit_solvent, bool):
            return implicit_solvent
    elif caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return implicit_solvent
    elif isinstance(implicit_solvent, str):
        return implicit_solvent

    raise ArgumentError('implicit_solvent', value=implicit_solvent, caller=caller, message=None)

