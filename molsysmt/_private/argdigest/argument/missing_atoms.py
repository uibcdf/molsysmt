from molsysmt._private.smonitor import ArgumentError


def digest_missing_atoms(missing_atoms, caller=None):
    if isinstance(missing_atoms, str) and missing_atoms in {"error", "omit"}:
        return missing_atoms
    raise ArgumentError("missing_atoms", value=missing_atoms, caller=caller)
