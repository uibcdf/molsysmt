from molsysmt._private.smonitor import ArgumentError

# The minimization backend exposes one algorithm through LocalEnergyMinimizer.
_supported_methods = {"l-bfgs": "L-BFGS"}


def digest_method(method, caller=None):
    """Validating the caller's named scientific method.

    Parameters
    ----------
    method : str
        The name of the method.

    caller : str, optional
        Name of the function or method that is being digested.

    Returns
    -------
    str
        The canonical name of the method.

    Raises
    ------
    ArgumentError
        If the method is not a string or its name is not supported.
    """

    if caller in {
        "molsysmt.topology.get_rings.get_rings",
        "molsysmt.physchem.get_aromatic_rings.get_aromatic_rings",
    }:
        if isinstance(method, str) and method == "minimum_cycle_basis":
            return method
        raise ArgumentError("method", value=method, caller=caller)

    if caller == "molsysmt.interactions.ionic.get_ionic_interactions.get_ionic_interactions":
        if isinstance(method, str) and method == "minimum_distance":
            return method
        raise ArgumentError("method", value=method, caller=caller)

    if caller in {
        "molsysmt.interactions.pi_pi.get_pi_pi_interactions.get_pi_pi_interactions",
    }:
        if isinstance(method, str) and method in {"centroid_angle_offset", "prolif", "molstar_geometry", "mdtraj_geometry"}:
            return method
        raise ArgumentError("method", value=method, caller=caller)

    if caller == "molsysmt.interactions.cation_pi.get_cation_pi_interactions.get_cation_pi_interactions":
        if isinstance(method, str) and method in {"prolif", "centroid_angle_offset", "molstar_geometry"}:
            return method
        raise ArgumentError("method", value=method, caller=caller)

    if caller == "molsysmt.physchem.get_hbond_sites.get_hbond_sites":
        if isinstance(method, str) and method in {"prolif", "cpptraj", "mdtraj"}:
            return method
        raise ArgumentError("method", value=method, caller=caller)

    if caller == "molsysmt.interactions.hbonds.get_hbonds.get_hbonds":
        if isinstance(method, str) and method in {"prolif", "cpptraj", "baker_hubbard", "wernet_nilsson", "mdanalysis_geometry"}:
            return method
        raise ArgumentError("method", value=method, caller=caller)

    if isinstance(method, str):
        try:
            return _supported_methods[method.lower()]
        except KeyError:
            pass

    raise ArgumentError("method", value=method, caller=caller, message=None)
