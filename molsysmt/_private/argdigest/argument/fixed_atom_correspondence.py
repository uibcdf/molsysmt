"""Digest optional partial chemical correspondence anchors."""


def digest_fixed_atom_correspondence(fixed_atom_correspondence, caller=None):
    from molsysmt.chemical_states._correspondence_constraints import normalize_pairs

    if fixed_atom_correspondence is None:
        return None
    return normalize_pairs(
        fixed_atom_correspondence, "fixed_atom_correspondence", caller
    )
