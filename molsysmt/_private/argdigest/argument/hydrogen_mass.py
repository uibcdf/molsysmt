from molsysmt._private.smonitor import ArgumentError

def digest_hydrogen_mass(hydrogen_mass, caller=None):


    if caller is not None and caller.startswith('molsysmt.form.') and '.to_' in caller:
        return hydrogen_mass

    raise ArgumentError('hydrogen_mass', value=hydrogen_mass, caller=caller, message=None)

