from molsysmt._private.smonitor import ArgumentError


def digest_pH(pH, caller=None):

    if pH is None and caller == 'molsysmt.build.add_missing_hydrogens.add_missing_hydrogens':
        return None

    if isinstance(pH, (int, float)):
        return pH

    raise ArgumentError("pH", value=pH, caller=caller, message=None)
