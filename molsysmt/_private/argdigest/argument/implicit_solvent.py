from molsysmt._private.smonitor import ArgumentError

def digest_implicit_solvent(implicit_solvent, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(implicit_solvent, bool):
            return implicit_solvent
    elif caller=='molsysmt.basic.convert.convert':
        if implicit_solvent is None:
            return implicit_solvent
    elif caller is not None and caller.startswith('molsysmt.form.') and '.to_' in caller:
        if implicit_solvent is None:
            return implicit_solvent

    if isinstance(implicit_solvent, str):
        from molsysmt.molecular_mechanics.forcefields import implicit_solvent_models
        if implicit_solvent in implicit_solvent_models:
            return implicit_solvent

    raise ArgumentError('implicit_solvent', value=implicit_solvent, caller=caller, message=None)

