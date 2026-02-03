from molsysmt._private.exceptions import ArgumentError

def digest_hydrogen_mass(hydrogen_mass, caller=None):


    if caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return hydrogen_mass

    raise ArgumentError('hydrogen_mass', value=hydrogen_mass, caller=caller, message=None)

