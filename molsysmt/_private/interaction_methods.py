"""Resolve scientific criteria separately from reproducible implementation profiles.

The implementation keys are private dispatch labels, retained to avoid changing
the already validated numerical kernels. Public names do not claim that a
reference software package invented the scientific criterion.
"""

from molsysmt._private.smonitor import ArgumentError

PROFILES = {
    "hbonds": {
        ("baker_hubbard", "nitrogen_oxygen"): "baker_hubbard",
        ("wernet_nilsson", "nitrogen_oxygen"): "wernet_nilsson",
        ("donor_acceptor_distance_angle", "elemental_fon"): "cpptraj",
        ("donor_acceptor_distance_angle", "smarts_donor_acceptor"): "prolif",
        ("donor_acceptor_distance_angle", "explicit_sites"): "mdanalysis_geometry",
    },
    "cation_pi": {
        ("centroid_distance_angle", "smarts_5_6"): "prolif",
        ("centroid_distance_offset", "three_atom_plane"): "molstar_geometry",
        ("centroid_angle_offset", "least_squares"): "centroid_angle_offset",
    },
    "pi_pi": {
        ("plane_angle_intersection", "smarts_5_6"): "prolif",
        ("plane_angle_intersection", "aromatic_cycles"): "mdtraj_geometry",
        ("centroid_angle_offset", "three_atom_plane"): "molstar_geometry",
        ("centroid_angle_offset", "least_squares"): "centroid_angle_offset",
    },
    "hbond_sites": {
        ("elemental_nitrogen_oxygen", None): "mdtraj",
        ("elemental_fluorine_oxygen_nitrogen", None): "cpptraj",
        ("smarts_donor_acceptor", None): "prolif",
    },
}

DEFAULT_PROFILES = {
    "baker_hubbard": "nitrogen_oxygen",
    "wernet_nilsson": "nitrogen_oxygen",
    "donor_acceptor_distance_angle": "elemental_fon",
    "centroid_distance_angle": "smarts_5_6",
    "centroid_distance_offset": "three_atom_plane",
    "centroid_angle_offset": "least_squares",
    "plane_angle_intersection": "smarts_5_6",
}


def supported_methods(family):
    """Return canonical names and the historical software selector aliases."""
    definitions = PROFILES[family]
    return {method for method, _ in definitions} | set(definitions.values())


def resolve_method(family, method, profile=None, *, caller=None):
    """Return canonical method, profile and the unchanged kernel dispatch key."""
    definitions = PROFILES[family]
    canonical = {name for name, _ in definitions}
    if method not in canonical:
        matches = [pair for pair, key in definitions.items() if key == method]
        if not matches:
            raise ArgumentError("method", value=method, caller=caller)
        name, implied = matches[0]
        if profile is not None and profile != implied:
            raise ArgumentError("profile", value=profile, caller=caller,
                                message="A compatibility alias already fixes its profile.")
        pair = (name, implied)
    else:
        pair = (method, DEFAULT_PROFILES.get(method) if profile is None else profile)
    if pair not in definitions:
        raise ArgumentError("profile", value=profile, caller=caller,
                            message="Choose a documented profile for this scientific method.")
    return dict(method=pair[0], profile=pair[1], implementation=definitions[pair],
                definition=f"molsysmt.{family}.{pair[0]}.{pair[1] or 'default'}@1")
