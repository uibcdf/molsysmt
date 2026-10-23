from molsysmt._private.smonitor import ArgumentError


def digest_atom_maps(atom_maps, caller=None):
    if isinstance(atom_maps, (list, tuple)) and atom_maps and all(
        isinstance(item, dict) for item in atom_maps
    ):
        return atom_maps
    raise ArgumentError("atom_maps", value=atom_maps, caller=caller)
