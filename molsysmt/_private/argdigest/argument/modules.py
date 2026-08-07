from molsysmt._private.smonitor import ArgumentError


def digest_modules(modules, caller=None):
    if isinstance(modules, bool):
        return modules

    raise ArgumentError("modules", value=modules, caller=caller, message=None)
