from molsysmt._private.smonitor import ArgumentError

def digest_dispersion_correction(dispersion_correction, caller=None):


    if caller is not None and caller.startswith('molsysmt.form.') and '.to_' in caller:
        return dispersion_correction
    elif isinstance(dispersion_correction, bool):
        return dispersion_correction

    raise ArgumentError('dispersion_correction', value=dispersion_correction, caller=caller, message=None)

