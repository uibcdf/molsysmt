"""Validate a caller-declared original map for positional RMSD reporting."""

from .atom_correspondence import digest_atom_correspondence


def digest_baseline_atom_correspondence(baseline_atom_correspondence, caller=None):
    if baseline_atom_correspondence is None:
        return None
    return digest_atom_correspondence(baseline_atom_correspondence, caller=caller)
