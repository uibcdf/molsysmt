from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentChoiceError, ArgumentError


@signal(tags=["molecular_mechanics"])
@arg_digest()
def get_engine_forcefield(
    forcefield,
    implicit_solvent=None,
    water_model=None,
    engine="OpenMM",
    skip_digestion=False,
):
    """
    Getting an independent list of engine-specific force-field resource names.

    Parameters
    ----------
    forcefield : str
        Registered force-field name, such as 'AMBER14' or 'CHARMM36'.
    implicit_solvent : str, default=None
        Physical implicit-solvent model: 'OBC1' or 'OBC2', subject to the
        selected engine/force-field mapping. If supplied, takes precedence
        over water_model. By default, no implicit-solvent model is selected.
    water_model : str, default=None
        Registered water-model name, such as 'TIP3P'. Used only when
        implicit_solvent is None. By default, no water model is selected.
    engine : str, default='OpenMM'
        Resource namespace: 'OpenMM' for XML names or 'LEaP' for leaprc names.
        Looking up metadata does not require the engine to be installed.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of str
        Ordered resource names for the requested engine, force field and model.
        Each call owns a new list. Editing it changes neither the registry nor
        results returned by other calls. No engine object is constructed.

    Raises
    ------
    ArgumentError
        If a name or argument type is invalid.
    ArgumentChoiceError
        If the engine/force-field/model combination has no registered entry.

    Notes
    -----
    With neither solvent argument supplied, the vacuum entry is returned.
    Entries are resource-name metadata, not a check that files exist or that
    an engine has completely configured a physical model. The OpenMM adapter
    maps OBC1 and OBC2 to distinct model XMLs. LEaP resource names only prepare
    topology/parameters; they do not set a subsequent simulation's igb option.
    Actual construction and parameterization occur in the consuming engine.

    Examples
    --------
    >>> import molsysmt as msm
    >>> resources = msm.molecular_mechanics.get_engine_forcefield(
    ...     'AMBER14', water_model='TIP3P')
    >>> resources
    ['amber14-all.xml', 'amber14/tip3p.xml']
    >>> resources.clear()
    >>> msm.molecular_mechanics.get_engine_forcefield('AMBER14', water_model='TIP3P')
    ['amber14-all.xml', 'amber14/tip3p.xml']
    >>> msm.molecular_mechanics.get_engine_forcefield('GAFF', engine='LEaP')
    ['leaprc.gaff']
    >>> msm.molecular_mechanics.get_engine_forcefield('AMBER14', implicit_solvent='OBC2')
    ['amber14-all.xml', 'implicit/obc2.xml']

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_engine_forcefield` for resource lookup and
       independent result ownership.

    .. versionadded:: 1.0.0
    """

    from .forcefields import switcher

    caller = "molsysmt.molecular_mechanics.get_engine_forcefield.get_engine_forcefield"
    if not isinstance(skip_digestion, bool):
        raise ArgumentError("skip_digestion", value=skip_digestion, caller=caller)

    if engine not in switcher:
        raise ArgumentChoiceError("engine", engine, list(switcher), caller=caller)
    fields = switcher[engine]
    if forcefield not in fields:
        raise ArgumentChoiceError("forcefield", forcefield, list(fields), caller=caller)

    if implicit_solvent is not None:
        model, argument = implicit_solvent, "implicit_solvent"
    elif water_model is not None:
        model, argument = water_model, "water_model"
    else:
        model, argument = "vacuum", "forcefield"

    models = fields[forcefield]
    if model not in models:
        raise ArgumentChoiceError(argument, model, list(models), caller=caller)

    return list(models[model])
