def get_engine_forcefield(forcefield, implicit_solvent=None, water_model=None, engine='OpenMM', skip_digestion=False):
    """
    Getting the engine-specific force field or simulation object from a molecular system.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form.
    engine : str, default='OpenMM'
        Target simulation engine backend.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

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

