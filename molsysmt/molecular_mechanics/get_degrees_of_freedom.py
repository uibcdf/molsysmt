from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest()
def get_degrees_of_freedom(molecular_system, forcefield='AMBER14', water_model=None, implicit_solvent=None, skip_digestion=False):
    """
    Calculating the mechanical degrees of freedom for a molecular system.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    forcefield : str, default='AMBER14'
        Force field parameter identifier or name.
    water_model : str, default=None
        Water model parameter identifier (e.g., 'TIP3P').
    implicit_solvent : str, default=None
        Implicit solvent model name if applicable.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    int
        The total number of mechanical degrees of freedom ($3 N_{	ext{particles}} - N_{	ext{constraints}}$).


    .. versionadded:: 1.0.0
    """
    from molsysmt import get_form, convert

    form_in = get_form(molecular_system)

    if form_in == "openmm.System":
        return 3 * molecular_system.getNumParticles() - molecular_system.getNumConstraints()
    else:
        try:
            kwargs = {}
            if forcefield is not None:
                kwargs['forcefield'] = forcefield
            if water_model is not None:
                kwargs['water_model'] = water_model
            if implicit_solvent is not None:
                kwargs['implicit_solvent'] = implicit_solvent

            system = convert(molecular_system, to_form='openmm.System', **kwargs)
            return 3 * system.getNumParticles() - system.getNumConstraints()
        except Exception:
            raise NotImplementedMethodError(caller="molsysmt.molecular_mechanics.get_degrees_of_freedom")
