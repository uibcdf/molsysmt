from molsysmt._private.exceptions import ArgumentError

def digest_salt_concentration(salt_concentration, caller=None):


    if caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return salt_concentration

    raise ArgumentError('salt_concentration', value=salt_concentration, caller=caller, message=None)

