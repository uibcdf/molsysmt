from molsysmt._private.smonitor import ArgumentError


def digest_atom_map(atom_map, caller=None):
    if isinstance(atom_map, dict):
        return atom_map
    raise ArgumentError("atom_map", value=atom_map, caller=caller)
