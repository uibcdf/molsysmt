from molsysmt._private.argdigest import arg_digest

@arg_digest()
def get_engine_forcefield(molecular_system, engine='OpenMM', skip_digestion=False):
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

    from molsysmt.basic import get_form

    form_in = get_form(molecular_system)

    if engine == 'OpenMM':

        if form_in in ['openmm.System', 'openmm.Context', 'openmm.Simulation']:
            return molecular_system

        from molsysmt.basic import convert
        return convert(molecular_system, to_form='openmm.System')

    else:
        raise NotImplementedError
