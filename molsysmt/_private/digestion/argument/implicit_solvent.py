from molsysmt._private.exceptions import ArgumentError

def digest_implicit_solvent(implicit_solvent, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(implicit_solvent, bool):
            return implicit_solvent
    elif caller=='molsysmt.basic.convert.convert':
        if implicit_solvent is None:
            return implicit_solvent
    elif caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        if implicit_solvent is None:
            return implicit_solvent

    if isinstance(implicit_solvent, str):
        from molsysmt.attribute import attributes
        if implicit_solvent in attributes['implicit_solvent']['values']:
            return implicit_solvent

    raise ArgumentError('implicit_solvent', value=implicit_solvent, caller=caller, message=None)

