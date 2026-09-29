"""Shared validation for complete-domain dictionary conversions."""

from molsysmt._private.variables import is_all


def require_full_domain(atom_indices, structure_indices):
    """Reject silent selection when the dictionary represents a full domain."""

    if not is_all(atom_indices) or not is_all(structure_indices):
        raise ValueError(
            "This conversion requires all atom and structure indices; "
            "query or extract the source explicitly before converting."
        )
