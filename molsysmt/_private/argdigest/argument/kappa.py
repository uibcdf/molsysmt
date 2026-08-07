from molsysmt._private.smonitor import ArgumentError

def digest_kappa(kappa, caller=None):


    if caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return kappa

    raise ArgumentError('kappa', value=kappa, caller=caller, message=None)

