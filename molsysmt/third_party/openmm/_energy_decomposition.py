"""Evaluate identifiable OpenMM force contributions without editing the source."""

from collections import Counter
from copy import copy
from math import fsum, isclose, isfinite

from molsysmt._private.smonitor import (
    NotImplementedMethodError,
    StructuralInconsistencyError,
)

_CALLER = "molsysmt.molecular_mechanics.get_potential_energy"


def _force_keys(forces):
    names = [force.getName() for force in forces]
    counts = Counter(names)
    reserved = set(names)
    for index, name in enumerate(names):
        if counts[name] == 1:
            yield name
            continue
        key = f"{name} [force {index}]"
        while key in reserved:
            key += f" [force {index}]"
        reserved.add(key)
        yield key


def _groups(force, nonbonded_type):
    direct = force.getForceGroup()
    if not isinstance(force, nonbonded_type):
        return {direct}
    method = force.getNonbondedMethod()
    groups = {direct} if force.getIncludeDirectSpace() else set()
    if method in (force.Ewald, force.PME, force.LJPME):
        reciprocal = force.getReciprocalSpaceForceGroup()
        groups.add(direct if reciprocal == -1 else reciprocal)
    return groups


def _isolated(groups):
    return len(set().union(*groups)) == sum(map(len, groups))


def _independent_context(context, forces, snapshot, openmm):
    if len(forces) > 32:
        raise NotImplementedMethodError(
            method="OpenMM per-force energy decomposition",
            message="The constructed OpenMM model has more than 32 forces. "
            "Per-force decomposition requires a distinct group for each force.",
            caller=_CALLER,
        )
    system = copy(context.getSystem())
    for index, force in enumerate(system.getForces()):
        force.setForceGroup(index)
        if isinstance(force, openmm.NonbondedForce):
            force.setReciprocalSpaceForceGroup(-1)
    platform = context.getPlatform()
    properties = {
        name: platform.getPropertyValue(context, name)
        for name in platform.getPropertyNames()
    }
    evaluation = openmm.Context(
        system, openmm.VerletIntegrator(0.001), platform, properties
    )
    evaluation.setState(snapshot)
    return evaluation


def decompose_potential_energy(context, *, constructed):
    """Read per-force energies from the live context or an isolated new model."""
    import openmm
    from openmm import unit

    forces = context.getSystem().getForces()
    groups = [_groups(force, openmm.NonbondedForce) for force in forces]
    if _isolated(groups):
        snapshot = context.getState(getEnergy=True)
        evaluation = context
    elif constructed:
        snapshot = context.getState(
            getPositions=True, getParameters=True, getEnergy=True
        )
        evaluation = _independent_context(context, forces, snapshot, openmm)
        groups = [{index} for index in range(len(forces))]
    else:
        raise NotImplementedMethodError(
            method="OpenMM per-force energy decomposition",
            message="Per-force decomposition is unavailable with overlapping force "
            "groups in the live OpenMM Context. Assign each force distinct groups "
            "before constructing the Context or request the total potential energy.",
            caller=_CALLER,
        )

    zero = 0.0 * unit.kilojoule_per_mole
    energies = {
        key: (
            evaluation.getState(getEnergy=True, groups=mask).getPotentialEnergy()
            if mask
            else zero
        )
        for key, mask in zip(_force_keys(forces), groups, strict=True)
    }
    total = snapshot.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
    terms = [
        energy.value_in_unit(unit.kilojoule_per_mole) for energy in energies.values()
    ]
    if (
        not isfinite(total)
        or not all(map(isfinite, terms))
        or not isclose(fsum(terms), total, rel_tol=1e-6, abs_tol=1e-5)
    ):
        raise StructuralInconsistencyError(
            "The OpenMM force contributions do not reproduce the finite Context "
            "potential energy. Check that force groups reflect the initialized "
            "model and the platform supports their independent evaluation.",
            caller=_CALLER,
        )
    return energies
