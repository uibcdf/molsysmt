from molsysmt._private.exceptions import ArgumentError

def digest_dispersion_correction(dispersion_correction, caller=None):


    if caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return dispersion_correction
    elif isinstance(dispersion_correction, bool):
        return dispersion_correction

    raise ArgumentError('dispersion_correction', value=dispersion_correction, caller=caller, message=None)

