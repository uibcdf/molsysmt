def get_engine_forcefield(forcefield, implicit_solvent=None, water_model=None, engine='OpenMM', skip_digestion=False):

    from .forcefields import switcher

    forcefield_out = None

    if implicit_solvent is not None:
        forcefield_out = switcher[engine][forcefield][implicit_solvent]
    elif water_model is not None:
        forcefield_out = switcher[engine][forcefield][water_model]
    else:
        forcefield_out = switcher[engine][forcefield]['vacuum']

    return forcefield_out

