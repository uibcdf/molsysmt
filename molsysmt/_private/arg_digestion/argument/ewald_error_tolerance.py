from molsysmt._private.exceptions import ArgumentError

def digest_ewald_error_tolerance(ewald_error_tolerance, caller=None):


    if caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return ewald_error_tolerance

    if ewald_error_tolerance is None:
        return ewald_error_tolerance

    if isinstance(ewald_error_tolerance, float):
        return ewald_error_tolerance

    raise ArgumentError('ewald_error_tolerance', value=ewald_error_tolerance, caller=caller, message=None)

