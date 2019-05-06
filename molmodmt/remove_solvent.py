"""

Remove Atoms
==============
Methods to remove atoms from a molecular model.


"""


def remove (item, selection=None, syntaxis='mdtraj'):

    """
    Remove a set of atoms from the molecular model

    Parameters
    ----------
    item : molecular model
        Molecular model in any form to be operated by the method.
    selection : str, int, list, tuple or numpy array
        Selection sentence or atoms indices list.
    Attributes
    ----------
    lambda_restraints
    Examples
    --------
    Create a system in a thermodynamic state.
    >>> from openmmtools import testsystems, states
    >>> system_container = testsystems.LysozymeImplicit()
    >>> system, positions = system_container.system, system_container.positions
    >>> thermodynamic_state = states.ThermodynamicState(system, 300*unit.kelvin)
    >>> sampler_state = states.SamplerState(positions)
    Identify ligand atoms. Topography automatically identify receptor atoms too.
    >>> from yank.yank import Topography
    >>> topography = Topography(system_container.topology, ligand_atoms=range(2603, 2621))
    Apply a Harmonic restraint between receptor and protein. Let the restraint
    automatically determine all the parameters.
    >>> restraint = Harmonic()
    >>> restraint.determine_missing_parameters(thermodynamic_state, sampler_state, topography)
    >>> restraint.restrain_state(thermodynamic_state)
    Create a ``RestraintState`` object to control the strength of the restraint.
    >>> restraint_state = RestraintState(lambda_restraints=1.0)
    ``RestraintState`` implements the ``IComposableState`` interface, so it can be
    used with ``CompoundThermodynamicState``.
    >>> compound_state = states.CompoundThermodynamicState(thermodynamic_state=thermodynamic_state,
    ...                                                    composable_states=[restraint_state])
    >>> compound_state.lambda_restraints
    1.0
    >>> integrator = openmm.VerletIntegrator(1.0*unit.femtosecond)
    >>> context = compound_state.create_context(integrator)
    >>> context.getParameter('lambda_restraints')
    1.0
    You can control the parameters in the OpenMM Context by setting the state's
    attributes. To To deactivate the restraint, set `lambda_restraints` to 0.0.
    >>> compound_state.lambda_restraints = 0.0
    >>> compound_state.apply_to_context(context)
    >>> context.getParameter('lambda_restraints')
    0.0
    """


    from .multitool import select as _select
    from .multitool import extract as _extract

    atoms_list_to_be_removed = _select(item, selection, syntaxis=syntaxis)
    atoms_list_all = _select(item, 'all', 'mdtraj')
    atoms_list_survive = list(set(atoms_list_all) - set(atoms_list_to_be_removed))

    return _extract(item, atoms_list_survive)


def remove_solvent (item, ions=False, include_selection=None, exclude_selection=None,
                   syntaxis='mdtraj'):

    from .multitool import select as _select
    from .utils.types import water_residues as _water_residues
    from .utils.types import ion_residues as _ion_residues

    atoms_list_to_be_removed = []
    atoms_list_water = []
    atoms_list_ions = []
    atoms_list_included = []
    atoms_list_excluded = []

    atoms_list_water = _select(item, 'resname '+' '.join([str(ii) for ii in _water_residues]),
                               syntaxis='mdtraj')

    if ions:
        atoms_list_ions = _select(item, 'resname '+' '.join([str(ii) for ii in _ion_residues]),
                                  syntaxis='mdtraj')

    if include_selection is not None:
        atoms_list_included = _select(item, include_selection, syntaxis=syntaxis)

    if exclude_selection is not None:
        atoms_list_excluded = _select(item, exclude_selection, syntaxis=syntaxis)

    atoms_list_to_be_removed = list(set(atoms_list_water) | set(atoms_list_ions) | set(atoms_list_included))
    atoms_list_to_be_removed = list(set(atoms_list_to_be_removed) - set(atoms_list_excluded))

    return _extract(item, atoms_list_to_be_removed)
