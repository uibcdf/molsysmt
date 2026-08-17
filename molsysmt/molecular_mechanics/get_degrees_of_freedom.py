from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest()
def get_degrees_of_freedom(molecular_system, forcefield='AMBER14', water_model=None, implicit_solvent=None, skip_digestion=False):
    """
    Calculating the mechanical degrees of freedom for a molecular system.

    Parameters
    ----------
    molecular_system : molecular system
        Input molecular system in any supported form (e.g. ``openmm.System``,
        ``openmm.Modeller``, ``pdbfixer.PDBFixer``, or native MolSysMT objects).
    forcefield : str, default 'AMBER14'
        Forcefield used to parametrize the system and identify constraints.
    water_model : str or None, default None
        Water model used if system contains solvent.
    implicit_solvent : str or None, default None
        Implicit solvent model if applicable.
    skip_digestion : bool, default False
        Whether to skip argument validation.

    Returns
    -------
    int
        The total number of mechanical degrees of freedom ($3 N_{\text{particles}} - N_{\text{constraints}}$).

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
