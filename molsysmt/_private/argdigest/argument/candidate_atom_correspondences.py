"""Digest optional complete candidate atom-index maps."""


def digest_candidate_atom_correspondences(candidate_atom_correspondences, caller=None):
    from molsysmt.topology._correspondence_constraints import normalize_candidates

    if candidate_atom_correspondences is None:
        return None
    return normalize_candidates(candidate_atom_correspondences, caller)
