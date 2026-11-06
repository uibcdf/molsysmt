# =======================
# Potential Energy
# =======================

"""
Potential Energy
================

Methods related with the potential energy of the system.
From energy minimization to potential energy contribution of specific set of atoms or interactions.
"""

import numpy as np
from depdigest import dep_digest

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import (
    ArgumentConflictError,
    ArgumentError,
    NotImplementedMethodError,
)
from molsysmt._private.variables import is_iterable_of_iterables


@arg_digest()
@dep_digest("openmm", when={"engine": "OpenMM"})
def get_non_bonded_potential_energy(
    molecular_system,
    selection="all",
    selection_2=None,
    platform="CPU",
    engine="OpenMM",
    syntax="MolSysMT",
    skip_digestion=False,
):
    """
    Calculating non-bonded potential energy within or between atom selections.

    With two disjoint atom sets A and B, evaluate E(A union B)-E(A)-E(B)
    using the configured engine's standard non-bonded force. A partitioned
    input requests one matrix entry per pair of sets, not per structure.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection, or a list of atom selections defining matrix rows.
        Numeric selections and MolSysMT selection strings are supported;
        other syntaxes retain their ordinary selector input restrictions.
        Repeated indices within a set are deduplicated. Repeated partitions
        and shared members within this axis are allowed.
    selection_2 : str, list, tuple, or numpy.ndarray, default=None
        Atom selection, or a list of selections defining matrix columns.
        No atom may belong to both axes. With None, calculate the internal
        non-bonded energy of one flat selection instead.
    platform : str, default='CPU'
        Execution platform name understood by the selected engine. OpenMM
        examples include 'Reference', 'CPU', 'CUDA' and 'OpenCL'; registered
        plugins are also admitted. Names are case-sensitive in this adapter.
        Selects newly constructed contexts; existing Context/Simulation inputs
        retain their actual platform. Unknown names and known unavailable
        platforms have separate native diagnostics. Device failures propagate.
    engine : str, default='OpenMM'
        Computation engine. Currently only 'OpenMM' is implemented.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity
        Scalar energy for flat/flat inputs or an internal energy request.
        If either input is partitioned, shape is (n_rows, n_columns), including
        a singleton axis for a flat input. Units follow the active PyUnitWizard
        policy (kJ/mol by default). Empty sets give exact typed zero entries;
        [] is one flat empty set and [[], []] defines two empty partitions.


    Raises
    ------
    ExecutionPlatformUnavailableError
        If a recognized execution platform is not registered by the engine.
    ArgumentChoiceError
        If a requested platform name is unknown to the selected engine.
    LibraryNotFoundError
        If the selected execution engine is not installed.
    ArgumentConflictError
        If the axes share atoms or a partitioned input has no second selection.
    ArgumentError
        If atom indices or partition nesting are invalid.
    NotImplementedMethodError
        If the engine model does not have exactly one standard non-bonded force.

    Notes
    -----
    Source selections, coordinates, engine parameters and force groups are not
    edited. A temporary engine System uses the supported public copy route.
    OpenMM decomposes NonbondedForce, including its exceptions; custom and
    implicit-solvent force contributions are not part of this result.
    Periodic energies retain their configured engine method and box; they are
    not an isolated pair potential or a binding free energy. Numerical partition
    parity is tested on nonperiodic NoCutoff models, not every periodic/custom
    model. Extract a specific structure before calling: this function does not
    loop over a structure axis. Context/Simulation inputs use current positions.

    See Also
    --------
    molsysmt.basic.select
        Resolving atom selections independently of the molecular-system form.
    molsysmt.molecular_mechanics.get_potential_energy
        Calculating total energy, including the other configured forces.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'], structure_indices=0)
    >>> energy = msm.molecular_mechanics.get_non_bonded_potential_energy(
    ...     molsys, selection=[[0, 1], [2, 3]], selection_2=[10, 11], platform='Reference')
    >>> energy.shape
    (2, 1)

    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_Get_non_bonded_potential_energy` for partitioned
       selections, units and interpretation limits.

    .. versionadded:: 1.0.0
    """

    from depdigest import check_dependency

    from molsysmt import convert, copy, get_form, has_attribute, select
    from molsysmt.configure import default_attribute

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)
    partitions_1, nested_1 = _normalize_atom_partitions(atom_indices, "selection")
    atom_indices = partitions_1 if nested_1 else partitions_1[0]
    nested_2 = False
    if selection_2 is not None:
        atom_indices_2 = select(molecular_system, selection=selection_2, syntax=syntax)
        partitions_2, nested_2 = _normalize_atom_partitions(
            atom_indices_2, "selection_2"
        )
        atom_indices_2 = partitions_2 if nested_2 else partitions_2[0]
        members_1 = {i for partition in partitions_1 for i in partition}
        members_2 = {i for partition in partitions_2 for i in partition}
        if members_1 & members_2:
            raise ArgumentConflictError(
                "selection",
                "selection_2",
                reason="Nonbonded interaction decomposition requires disjoint atom sets between the two axes.",
                caller="molsysmt.molecular_mechanics.get_non_bonded_potential_energy",
            )
    else:
        if nested_1:
            raise ArgumentConflictError(
                "selection",
                "selection_2",
                reason="A partitioned selection requires an explicit second selection; internal energy accepts one flat selection.",
                caller="molsysmt.molecular_mechanics.get_non_bonded_potential_energy",
            )
        atom_indices_2 = None

    if engine == "OpenMM":
        check_dependency("openmm")
        import openmm as mm

        form_in = get_form(molecular_system)

        if form_in == "openmm.Context":
            context = molecular_system

        elif form_in == "openmm.Simulation":
            context = molecular_system.context

        else:
            extra_conversion_arguments = {}

            possible_missing_attributes = [
                "forcefield",
                "water_model",
                "implicit_solvent",
                "constraints",
                "non_bonded_method",
                "switch_distance",
                "dispersion_correction",
                "ewald_error_tolerance",
                "integrator",
                "temperature",
                "friction",
                "time_step",
            ]

            for att in possible_missing_attributes:
                if not has_attribute(molecular_system, att):
                    extra_conversion_arguments[att] = default_attribute[att]

            context = convert(
                molecular_system,
                to_form="openmm.Context",
                **extra_conversion_arguments,
                platform=platform,
            )

        # Parameter masking must never edit the caller's engine System.
        tmp_system = copy(context.getSystem())

        forces = list(tmp_system.getForces())
        non_bonded_forces = [
            force for force in forces if isinstance(force, mm.NonbondedForce)
        ]
        if len(non_bonded_forces) != 1:
            raise NotImplementedMethodError(
                method="nonbonded decomposition with exactly one OpenMM NonbondedForce",
                arguments={"n_nonbonded_forces": len(non_bonded_forces)},
                caller="molsysmt.molecular_mechanics.get_non_bonded_potential_energy",
            )
        for force in forces:
            force.setForceGroup(1)
        non_bonded_force = non_bonded_forces[0]
        non_bonded_forcegroup = 0
        non_bonded_force.setForceGroup(non_bonded_forcegroup)
        non_bonded_force.setReciprocalSpaceForceGroup(non_bonded_forcegroup)

        state = context.getState(getPositions=True)
        tmp_system.setDefaultPeriodicBoxVectors(*state.getPeriodicBoxVectors())
        tmp_context = mm.Context(
            tmp_system, mm.VerletIntegrator(0.001), context.getPlatform()
        )
        tmp_context.setPositions(state.getPositions())

        original_particle_parameters = {}
        for ii in range(non_bonded_force.getNumParticles()):
            charge, sigma, epsilon = non_bonded_force.getParticleParameters(ii)
            original_particle_parameters[ii] = {
                "charge": charge,
                "sigma": sigma,
                "epsilon": epsilon,
            }

        original_exception_parameters = {}
        for ii in range(non_bonded_force.getNumExceptions()):
            particle1, particle2, chargeProd, sigma, epsilon = (
                non_bonded_force.getExceptionParameters(ii)
            )
            original_exception_parameters[ii] = {
                "particle1": particle1,
                "particle2": particle2,
                "chargeProd": chargeProd,
                "sigma": sigma,
                "epsilon": epsilon,
            }

        if atom_indices_2 is None:
            output = _aux_openmm(
                atom_indices,
                non_bonded_force,
                non_bonded_forcegroup,
                tmp_context,
                original_particle_parameters,
                original_exception_parameters,
            )

            output = puw.standardize(output)

        else:
            if not nested_1 and not nested_2:
                output = _aux_openmm_crossed(
                    atom_indices,
                    atom_indices_2,
                    non_bonded_force,
                    non_bonded_forcegroup,
                    tmp_context,
                    original_particle_parameters,
                    original_exception_parameters,
                )

                output = puw.standardize(output)

            else:
                output = _aux_openmm_crossed_lists(
                    atom_indices,
                    atom_indices_2,
                    non_bonded_force,
                    non_bonded_forcegroup,
                    tmp_context,
                    original_particle_parameters,
                    original_exception_parameters,
                )

                output = puw.standardize(output)

        return output

    else:
        raise NotImplementedError


def _normalize_atom_partitions(atom_indices, argument):
    """Normalize resolved atom sets without losing empty or repeated partitions."""
    if atom_indices is None:
        raise ArgumentError(
            argument,
            value=atom_indices,
            caller="molsysmt.molecular_mechanics.get_non_bonded_potential_energy",
        )
    nested = bool(len(atom_indices)) and is_iterable_of_iterables(atom_indices)
    partitions = atom_indices if nested else [atom_indices]
    output = []
    for partition in partitions:
        if not all(isinstance(i, (int, np.integer)) for i in partition):
            raise ArgumentError(
                argument,
                value=atom_indices,
                caller="molsysmt.molecular_mechanics.get_non_bonded_potential_energy",
            )
        output.append(list(dict.fromkeys(partition)))
    return output, nested


def _aux_openmm(
    atoms_in,
    non_bonded_force,
    non_bonded_forcegroup,
    context,
    original_particle_parameters,
    original_exception_parameters,
):

    from openmm import unit

    if not atoms_in:
        return 0.0 * unit.kilojoule_per_mole

    for ii, parameters in original_particle_parameters.items():
        charge = parameters["charge"]
        sigma = parameters["sigma"]
        epsilon = parameters["epsilon"]

        if ii not in atoms_in:
            charge = 0.0 * unit.elementary_charge
            epsilon = 0.0 * unit.kilojoule_per_mole
            sigma = 0.0 * unit.nanometer

        non_bonded_force.setParticleParameters(ii, charge, sigma, epsilon)

    for ii, parameters in original_exception_parameters.items():
        particle1 = parameters["particle1"]
        particle2 = parameters["particle2"]
        chargeProd = parameters["chargeProd"]
        sigma = parameters["sigma"]
        epsilon = parameters["epsilon"]

        if (particle1 not in atoms_in) or (particle2 not in atoms_in):
            epsilon = 0.0 * unit.kilojoule_per_mole
            sigma = 0.0 * unit.nanometer
            if chargeProd != 0.0 * unit.elementary_charge**2:
                chargeProd = 1e-22 * unit.elementary_charge**2

        non_bonded_force.setExceptionParameters(
            ii, particle1, particle2, chargeProd, sigma, epsilon
        )

    non_bonded_force.updateParametersInContext(context)

    energy = context.getState(
        getEnergy=True, groups={non_bonded_forcegroup}
    ).getPotentialEnergy()

    return energy


def _aux_openmm_crossed(
    atoms_in_1,
    atoms_in_2,
    non_bonded_force,
    non_bonded_forcegroup,
    context,
    original_particle_parameters,
    original_exception_parameters,
):

    from openmm import unit

    if not atoms_in_1 or not atoms_in_2:
        return 0.0 * unit.kilojoule_per_mole

    aux_exc_pars_11 = []
    aux_exc_pars_22 = []
    aux_exc_pars_12 = []

    zero_charge = 0.0 * unit.elementary_charge
    zero_chargeProd = 0.0 * unit.elementary_charge**2
    zero_almost_chargeProd = 1e-22 * unit.elementary_charge**2
    zero_epsilon = 0.0 * unit.kilojoule_per_mole
    zero_sigma = 0.0 * unit.nanometer

    # All to zero

    for ii, parameters in original_particle_parameters.items():
        non_bonded_force.setParticleParameters(
            ii, zero_charge, zero_sigma, zero_epsilon
        )

    for ii, parameters in original_exception_parameters.items():
        particle1 = parameters["particle1"]
        particle2 = parameters["particle2"]
        chargeProd = parameters["chargeProd"]
        sigma = parameters["sigma"]
        epsilon = parameters["epsilon"]

        if (particle1 in atoms_in_1) and (particle2 in atoms_in_1):
            aux_exc_pars_11.append(
                [ii, particle1, particle2, chargeProd, sigma, epsilon]
            )

        elif (particle1 in atoms_in_2) and (particle2 in atoms_in_2):
            aux_exc_pars_22.append(
                [ii, particle1, particle2, chargeProd, sigma, epsilon]
            )

        elif ((particle1 in atoms_in_1) and (particle2 in atoms_in_2)) or (
            (particle1 in atoms_in_2) and (particle2 in atoms_in_1)
        ):
            aux_exc_pars_12.append(
                [ii, particle1, particle2, chargeProd, sigma, epsilon]
            )

        if chargeProd != 0.0 * unit.elementary_charge**2:
            non_bonded_force.setExceptionParameters(
                ii,
                particle1,
                particle2,
                zero_almost_chargeProd,
                zero_sigma,
                zero_epsilon,
            )
        else:
            non_bonded_force.setExceptionParameters(
                ii, particle1, particle2, zero_chargeProd, zero_sigma, zero_epsilon
            )

    non_bonded_force.updateParametersInContext(context)

    # subsystem1

    for ii in atoms_in_1:
        charge = original_particle_parameters[ii]["charge"]
        sigma = original_particle_parameters[ii]["sigma"]
        epsilon = original_particle_parameters[ii]["epsilon"]

        non_bonded_force.setParticleParameters(ii, charge, sigma, epsilon)

    for ii, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_11:
        non_bonded_force.setExceptionParameters(
            ii, particle1, particle2, chargeProd, sigma, epsilon
        )

    non_bonded_force.updateParametersInContext(context)

    energy_1 = context.getState(
        getEnergy=True, groups={non_bonded_forcegroup}
    ).getPotentialEnergy()

    # subsystem1 union subsystem2

    for ii in atoms_in_2:
        charge = original_particle_parameters[ii]["charge"]
        sigma = original_particle_parameters[ii]["sigma"]
        epsilon = original_particle_parameters[ii]["epsilon"]

        non_bonded_force.setParticleParameters(ii, charge, sigma, epsilon)

    for ii, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_22:
        non_bonded_force.setExceptionParameters(
            ii, particle1, particle2, chargeProd, sigma, epsilon
        )

    for ii, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_12:
        non_bonded_force.setExceptionParameters(
            ii, particle1, particle2, chargeProd, sigma, epsilon
        )

    non_bonded_force.updateParametersInContext(context)

    energy_12 = context.getState(
        getEnergy=True, groups={non_bonded_forcegroup}
    ).getPotentialEnergy()

    # subsystem2 (subsystem1 to zero)

    for ii in atoms_in_1:
        non_bonded_force.setParticleParameters(
            ii, zero_charge, zero_sigma, zero_epsilon
        )

    for ii, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_11:
        if chargeProd != 0.0 * unit.elementary_charge**2:
            non_bonded_force.setExceptionParameters(
                ii,
                particle1,
                particle2,
                zero_almost_chargeProd,
                zero_sigma,
                zero_epsilon,
            )
        else:
            non_bonded_force.setExceptionParameters(
                ii, particle1, particle2, zero_chargeProd, zero_sigma, zero_epsilon
            )

    for ii, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_12:
        if chargeProd != 0.0 * unit.elementary_charge**2:
            non_bonded_force.setExceptionParameters(
                ii,
                particle1,
                particle2,
                zero_almost_chargeProd,
                zero_sigma,
                zero_epsilon,
            )
        else:
            non_bonded_force.setExceptionParameters(
                ii, particle1, particle2, zero_chargeProd, zero_sigma, zero_epsilon
            )

    non_bonded_force.updateParametersInContext(context)

    energy_2 = context.getState(
        getEnergy=True, groups={non_bonded_forcegroup}
    ).getPotentialEnergy()

    energy = energy_12 - energy_1 - energy_2

    return energy


def _aux_openmm_crossed_lists(
    atoms_in_1,
    atoms_in_2,
    non_bonded_force,
    non_bonded_forcegroup,
    context,
    original_particle_parameters,
    original_exception_parameters,
):

    from openmm import unit

    if not atoms_in_1 or not is_iterable_of_iterables(atoms_in_1):
        atoms_in_1 = [atoms_in_1]

    if not atoms_in_2 or not is_iterable_of_iterables(atoms_in_2):
        atoms_in_2 = [atoms_in_2]

    n_atoms_lists_in_1 = len(atoms_in_1)
    n_atoms_lists_in_2 = len(atoms_in_2)

    aux_exc_pars_1 = [[] for ii in range(n_atoms_lists_in_1)]
    aux_exc_pars_2 = [[] for jj in range(n_atoms_lists_in_2)]
    aux_exc_pars_12 = [
        [[] for jj in range(n_atoms_lists_in_2)] for ii in range(n_atoms_lists_in_1)
    ]

    output = (
        np.zeros((n_atoms_lists_in_1, n_atoms_lists_in_2), dtype=float)
        * unit.kilojoule_per_mole
    )
    E1 = np.zeros((n_atoms_lists_in_1), dtype=float) * unit.kilojoule_per_mole
    E2 = np.zeros((n_atoms_lists_in_2), dtype=float) * unit.kilojoule_per_mole

    zero_charge = 0.0 * unit.elementary_charge
    zero_chargeProd = 0.0 * unit.elementary_charge**2
    zero_almost_chargeProd = 1e-22 * unit.elementary_charge**2
    zero_epsilon = 0.0 * unit.kilojoule_per_mole
    zero_sigma = 0.0 * unit.nanometer

    # All to zero

    inv_aux_dict_1 = {}
    inv_aux_dict_2 = {}

    for jj, aux in enumerate(atoms_in_1):
        for ii in aux:
            inv_aux_dict_1.setdefault(ii, set()).add(jj)

    for jj, aux in enumerate(atoms_in_2):
        for ii in aux:
            inv_aux_dict_2.setdefault(ii, set()).add(jj)

    for ii, parameters in original_particle_parameters.items():
        non_bonded_force.setParticleParameters(
            ii, zero_charge, zero_sigma, zero_epsilon
        )

    for ii, parameters in original_exception_parameters.items():
        particle1 = parameters["particle1"]
        particle2 = parameters["particle2"]
        chargeProd = parameters["chargeProd"]
        sigma = parameters["sigma"]
        epsilon = parameters["epsilon"]

        first_1 = inv_aux_dict_1.get(particle1, set())
        second_1 = inv_aux_dict_1.get(particle2, set())
        first_2 = inv_aux_dict_2.get(particle1, set())
        second_2 = inv_aux_dict_2.get(particle2, set())
        parameters = [ii, particle1, particle2, chargeProd, sigma, epsilon]
        for aa in sorted(first_1 & second_1):
            aux_exc_pars_1[aa].append(parameters)
        for bb in sorted(first_2 & second_2):
            aux_exc_pars_2[bb].append(parameters)
        for aa in sorted(first_1):
            for bb in sorted(second_2):
                aux_exc_pars_12[aa][bb].append(parameters)
        for aa in sorted(second_1):
            for bb in sorted(first_2):
                aux_exc_pars_12[aa][bb].append(parameters)

        if chargeProd != 0.0 * unit.elementary_charge**2:
            non_bonded_force.setExceptionParameters(
                ii,
                particle1,
                particle2,
                zero_almost_chargeProd,
                zero_sigma,
                zero_epsilon,
            )
        else:
            non_bonded_force.setExceptionParameters(
                ii, particle1, particle2, zero_chargeProd, zero_sigma, zero_epsilon
            )

    non_bonded_force.updateParametersInContext(context)

    # E1

    for ii, aux in enumerate(atoms_in_1):
        for jj in aux:
            charge = original_particle_parameters[jj]["charge"]
            sigma = original_particle_parameters[jj]["sigma"]
            epsilon = original_particle_parameters[jj]["epsilon"]

            non_bonded_force.setParticleParameters(jj, charge, sigma, epsilon)

        for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_1[ii]:
            non_bonded_force.setExceptionParameters(
                jj, particle1, particle2, chargeProd, sigma, epsilon
            )

        non_bonded_force.updateParametersInContext(context)

        E1[ii] = context.getState(
            getEnergy=True, groups={non_bonded_forcegroup}
        ).getPotentialEnergy()

        for jj in aux:
            non_bonded_force.setParticleParameters(
                jj, zero_charge, zero_sigma, zero_epsilon
            )

        for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_1[ii]:
            if chargeProd != 0.0 * unit.elementary_charge**2:
                non_bonded_force.setExceptionParameters(
                    jj,
                    particle1,
                    particle2,
                    zero_almost_chargeProd,
                    zero_sigma,
                    zero_epsilon,
                )
            else:
                non_bonded_force.setExceptionParameters(
                    jj, particle1, particle2, zero_chargeProd, zero_sigma, zero_epsilon
                )

    # E2

    for ii, aux in enumerate(atoms_in_2):
        for jj in aux:
            charge = original_particle_parameters[jj]["charge"]
            sigma = original_particle_parameters[jj]["sigma"]
            epsilon = original_particle_parameters[jj]["epsilon"]

            non_bonded_force.setParticleParameters(jj, charge, sigma, epsilon)

        for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_2[ii]:
            non_bonded_force.setExceptionParameters(
                jj, particle1, particle2, chargeProd, sigma, epsilon
            )

        non_bonded_force.updateParametersInContext(context)

        E2[ii] = context.getState(
            getEnergy=True, groups={non_bonded_forcegroup}
        ).getPotentialEnergy()

        for jj in aux:
            non_bonded_force.setParticleParameters(
                jj, zero_charge, zero_sigma, zero_epsilon
            )

        for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_2[ii]:
            if chargeProd != 0.0 * unit.elementary_charge**2:
                non_bonded_force.setExceptionParameters(
                    jj,
                    particle1,
                    particle2,
                    zero_almost_chargeProd,
                    zero_sigma,
                    zero_epsilon,
                )
            else:
                non_bonded_force.setExceptionParameters(
                    jj, particle1, particle2, zero_chargeProd, zero_sigma, zero_epsilon
                )

    # E1 + E2 + E12

    for ii, aux1 in enumerate(atoms_in_1):
        for jj in aux1:
            charge = original_particle_parameters[jj]["charge"]
            sigma = original_particle_parameters[jj]["sigma"]
            epsilon = original_particle_parameters[jj]["epsilon"]

            non_bonded_force.setParticleParameters(jj, charge, sigma, epsilon)

        for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_1[ii]:
            non_bonded_force.setExceptionParameters(
                jj, particle1, particle2, chargeProd, sigma, epsilon
            )

        for ll, aux2 in enumerate(atoms_in_2):
            for jj in aux2:
                charge = original_particle_parameters[jj]["charge"]
                sigma = original_particle_parameters[jj]["sigma"]
                epsilon = original_particle_parameters[jj]["epsilon"]

                non_bonded_force.setParticleParameters(jj, charge, sigma, epsilon)

            for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_2[
                ll
            ]:
                non_bonded_force.setExceptionParameters(
                    jj, particle1, particle2, chargeProd, sigma, epsilon
                )

            for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_12[
                ii
            ][ll]:
                non_bonded_force.setExceptionParameters(
                    jj, particle1, particle2, chargeProd, sigma, epsilon
                )

            non_bonded_force.updateParametersInContext(context)

            output[ii, ll] = context.getState(
                getEnergy=True, groups={non_bonded_forcegroup}
            ).getPotentialEnergy()

            for jj in aux2:
                non_bonded_force.setParticleParameters(
                    jj, zero_charge, zero_sigma, zero_epsilon
                )

            for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_2[
                ll
            ]:
                if chargeProd != 0.0 * unit.elementary_charge**2:
                    non_bonded_force.setExceptionParameters(
                        jj,
                        particle1,
                        particle2,
                        zero_almost_chargeProd,
                        zero_sigma,
                        zero_epsilon,
                    )
                else:
                    non_bonded_force.setExceptionParameters(
                        jj,
                        particle1,
                        particle2,
                        zero_chargeProd,
                        zero_sigma,
                        zero_epsilon,
                    )

            for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_12[
                ii
            ][ll]:
                if chargeProd != 0.0 * unit.elementary_charge**2:
                    non_bonded_force.setExceptionParameters(
                        jj,
                        particle1,
                        particle2,
                        zero_almost_chargeProd,
                        zero_sigma,
                        zero_epsilon,
                    )
                else:
                    non_bonded_force.setExceptionParameters(
                        jj,
                        particle1,
                        particle2,
                        zero_chargeProd,
                        zero_sigma,
                        zero_epsilon,
                    )

        for jj in aux1:
            non_bonded_force.setParticleParameters(
                jj, zero_charge, zero_sigma, zero_epsilon
            )

        for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_1[ii]:
            if chargeProd != 0.0 * unit.elementary_charge**2:
                non_bonded_force.setExceptionParameters(
                    jj,
                    particle1,
                    particle2,
                    zero_almost_chargeProd,
                    zero_sigma,
                    zero_epsilon,
                )
            else:
                non_bonded_force.setExceptionParameters(
                    jj, particle1, particle2, zero_chargeProd, zero_sigma, zero_epsilon
                )

    for ii in range(n_atoms_lists_in_1):
        for jj in range(n_atoms_lists_in_2):
            if atoms_in_1[ii] and atoms_in_2[jj]:
                output[ii, jj] = output[ii, jj] - E1[ii] - E2[jj]
            else:
                output[ii, jj] = 0.0 * unit.kilojoule_per_mole

    return output
