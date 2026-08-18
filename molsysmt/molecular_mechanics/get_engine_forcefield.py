def get_engine_forcefield(forcefield, implicit_solvent=None, water_model=None, engine='OpenMM', skip_digestion=False):
    """
    Getting the engine-specific force field or simulation object from a molecular system.




    Parameters
    ----------
    forcefield : str
        Force field parameter identifier or name.
    implicit_solvent : str, default=None
        Implicit solvent model name if applicable.
    water_model : str, default=None
        Water model parameter identifier (e.g., 'TIP3P').
    engine : object, default='OpenMM'
        Argument engine.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Engine-specific force field representation (e.g. `openmm.app.ForceField` or `openmm.System`).




    .. versionadded:: 1.0.0
    """

    from .forcefields import switcher

    forcefield_out = None

    if implicit_solvent is not None:
        forcefield_out = switcher[engine][forcefield][implicit_solvent]
    elif water_model is not None:
        forcefield_out = switcher[engine][forcefield][water_model]
    else:
        forcefield_out = switcher[engine][forcefield]['vacuum']

    return forcefield_out

