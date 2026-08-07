from molsysmt._private.argdigest.argument.atom_is_aromatic import (
    digest_atom_is_aromatic,
)


def digest_allows_implicit_hydrogens(allows_implicit_hydrogens, caller=None):
    return digest_atom_is_aromatic(allows_implicit_hydrogens, caller=caller)
