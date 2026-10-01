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

    families = {
        "molsysmt.interactions.metal_coordination.get_metal_coordination.get_metal_coordination": "metal_coordination",
        "molsysmt.physchem.get_metal_coordination_sites.get_metal_coordination_sites": "metal_coordination_sites",
        "molsysmt.interactions.water_bridges.get_water_bridges.get_water_bridges": "water_bridges",
        "molsysmt.physchem.get_water_sites.get_water_sites": "water_sites",

        "molsysmt.interactions.hydrophobic.get_hydrophobic_interactions.get_hydrophobic_interactions": "hydrophobic",
        "molsysmt.physchem.get_hydrophobic_sites.get_hydrophobic_sites": "hydrophobic_sites",
        "molsysmt.interactions.halogen_bonds.get_halogen_bonds.get_halogen_bonds": "halogen_bonds",
        "molsysmt.physchem.get_halogen_bond_sites.get_halogen_bond_sites": "halogen_bond_sites",
        "molsysmt.interactions.pi_pi.get_pi_pi_interactions.get_pi_pi_interactions": "pi_pi",
        "molsysmt.interactions.cation_pi.get_cation_pi_interactions.get_cation_pi_interactions": "cation_pi",
        "molsysmt.interactions.hbonds.get_hbonds.get_hbonds": "hbonds",
        "molsysmt.physchem.get_hbond_sites.get_hbond_sites": "hbond_sites",
    }
    if caller in families:
        from molsysmt._private.interaction_methods import supported_methods

        if isinstance(method, str) and method in supported_methods(families[caller]):
            return method
        raise ArgumentError("method", value=method, caller=caller)

    if isinstance(method, str):
        try:
            return _supported_methods[method.lower()]
        except KeyError:
            pass

    raise ArgumentError("method", value=method, caller=caller, message=None)
