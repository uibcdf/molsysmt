"""Declare physical adapter controls separately from execution settings."""

from copy import deepcopy

from molsysmt._private.smonitor import UnsupportedMechanicalControlError

SUPPORTED = (
    "forcefield",
    "water_model",
    "implicit_solvent",
    "constraints",
    "non_bonded_method",
    "switch_distance",
    "dispersion_correction",
    "ewald_error_tolerance",
)
UNSUPPORTED = (
    "cutoff_distance",
    "flexible_constraints",
    "rigid_water",
    "hydrogen_mass",
    "salt_concentration",
    "kappa",
    "solute_dielectric",
    "solvent_dielectric",
    "partial_charge",
    "atom_ff_type",
)
PARAMETERIZED = {"openmm.System", "openmm.Context", "openmm.Simulation"}
CONSTRUCTION_TARGETS = {"openmm.System", "openmm.Context", "openmm.Simulation"}


def forms(source):
    from molsysmt.basic import get_form

    result = get_form(source)
    return [result] if isinstance(result, str) else list(result)


def reject_unsupported(source, *, caller, overrides=None):
    from molsysmt.basic import has_attribute
    from molsysmt.native import MolecularMechanics, MolSys

    if PARAMETERIZED.intersection(forms(source)):
        return
    overrides = overrides or {}
    unsupported = [
        name
        for name in UNSUPPORTED
        if (name in overrides and overrides[name] is not None)
        or has_attribute(source, name)
    ]
    for part in source if isinstance(source, (list, tuple)) else [source]:
        mechanics = (
            part.molecular_mechanics
            if isinstance(part, MolSys)
            else part
            if isinstance(part, MolecularMechanics)
            else None
        )
        if mechanics is not None and mechanics.formal_charge is not None:
            unsupported.append("MolecularMechanics.formal_charge")
    if unsupported:
        raise UnsupportedMechanicalControlError(
            method="physical model construction", arguments=unsupported, caller=caller
        )

    requested(source, overrides=overrides, caller=caller)


def requested(
    source, overrides=None, caller="molsysmt.molecular_mechanics.get_model_recipe"
):
    from molsysmt._private.smonitor import ArgumentConflictError
    from molsysmt.basic import get, has_attribute
    from molsysmt.configure import default_attribute

    overrides = overrides or {}
    result, defaults = {}, {}
    for name in SUPPORTED:
        stored = has_attribute(source, name)
        if name in overrides:
            value, origin = overrides[name], "argument"
        elif stored:
            value, origin = get(source, **{name: True}), "stored"
        else:
            value, origin = default_attribute[name], "molsysmt_default"
        result[name] = dict(value=deepcopy(value), origin=origin)
        if not stored and name not in overrides:
            defaults[name] = value
    water, implicit = result["water_model"], result["implicit_solvent"]
    if water["value"] is not None and implicit["value"] is not None:
        water_explicit = water["origin"] != "molsysmt_default"
        implicit_explicit = implicit["origin"] != "molsysmt_default"
        if water_explicit and implicit_explicit:
            raise ArgumentConflictError(
                "water_model",
                "implicit_solvent",
                reason="The construction adapter requires one explicit solvent-model family.",
                caller=caller,
            )
        inactive = "implicit_solvent" if water_explicit else "water_model"
        entry = result[inactive]
        entry.update(
            inactive_default=entry["value"], value=None, origin="inapplicable_default"
        )
        defaults[inactive] = None
    return result, defaults


def context_defaults(source):
    from molsysmt.basic import has_attribute
    from molsysmt.configure import default_attribute

    if PARAMETERIZED.intersection(forms(source)):
        missing = {}
    else:
        _, missing = requested(source)
    for name in ("integrator", "temperature", "friction", "time_step"):
        if not has_attribute(source, name):
            missing[name] = default_attribute[name]
    return missing


def inspect_system(system):
    import numpy as np
    import openmm

    from molsysmt import pyunitwizard as puw

    methods = {
        openmm.NonbondedForce.NoCutoff: "no_cutoff",
        openmm.NonbondedForce.CutoffNonPeriodic: "cutoff_nonperiodic",
        openmm.NonbondedForce.CutoffPeriodic: "cutoff_periodic",
        openmm.NonbondedForce.Ewald: "ewald",
        openmm.NonbondedForce.PME: "particle_mesh_ewald",
        openmm.NonbondedForce.LJPME: "lennard_jones_particle_mesh_ewald",
    }

    def length(value):
        return puw.standardize(puw.quantity(puw.get_value(value, to_unit="nm"), "nm"))

    nonbonded = []
    force_types = []
    for force in system.getForces():
        force_types.append(type(force).__name__)
        if isinstance(force, openmm.NonbondedForce):
            method = methods[force.getNonbondedMethod()]
            switched = force.getUseSwitchingFunction()
            nonbonded.append(
                dict(
                    method=method,
                    cutoff_distance=None
                    if method == "no_cutoff"
                    else length(force.getCutoffDistance()),
                    switching_enabled=switched,
                    switch_distance=length(force.getSwitchingDistance())
                    if switched
                    else None,
                    dispersion_correction=force.getUseDispersionCorrection(),
                    ewald_error_tolerance=force.getEwaldErrorTolerance(),
                    reaction_field_dielectric=force.getReactionFieldDielectric(),
                )
            )
    periodic = system.usesPeriodicBoundaryConditions()
    box = None
    if periodic:
        from openmm import unit

        box = puw.standardize(
            puw.quantity(
                np.asarray(
                    [
                        row.value_in_unit(unit.nanometer)
                        for row in system.getDefaultPeriodicBoxVectors()
                    ]
                ),
                "nm",
            )
        )
    return dict(
        n_particles=system.getNumParticles(),
        n_constraints=system.getNumConstraints(),
        periodic=periodic,
        default_box=box,
        nonbonded=nonbonded,
        provider_force_types=force_types,
    )


def model_context(source, structure_indices, caller):
    """Read one physical construction context without a full modular trajectory."""
    import numpy as np

    from molsysmt._private.argdigest.argument._correspondence_axes import flat_axis
    from molsysmt._private.h5msm import modular_h5msm_dimensions
    from molsysmt._private.smonitor import ArgumentConflictError, ArgumentError
    from molsysmt._private.variables import is_all
    from molsysmt.basic import get, has_attribute

    parts = list(source) if isinstance(source, (list, tuple)) else [source]
    files = [
        (i, part, dims)
        for i, part in enumerate(parts)
        if (dims := modular_h5msm_dimensions(part)) is not None
    ]
    if len(files) > 1:
        raise ArgumentConflictError("molecular_system", "structures", caller=caller)
    count = files[0][2][1] if files else get(source, n_structures=True)
    if structure_indices is None:
        frames = [0] if count else []
    elif is_all(structure_indices):
        frames = list(range(count or 0))
    else:
        frames = flat_axis(structure_indices, "structure_indices", caller).tolist()
        if not frames or not count or any(v < 0 or v >= count for v in frames):
            raise ArgumentError(
                "structure_indices", value=structure_indices, caller=caller
            )
    if len(frames) > 1:
        raise ArgumentError("structure_indices", value=structure_indices, caller=caller)
    if files:
        i, filename, _ = files[0]
        if any(
            has_attribute(part, "coordinates") for j, part in enumerate(parts) if j != i
        ):
            raise ArgumentConflictError("molecular_system", "structures", caller=caller)
        from molsysmt.form._h5msm05_modular import _read_calculation_chemistry

        native, state = _read_calculation_chemistry(
            filename,
            chemical_state="structure" if frames else "reference",
            structure_indices=frames,
            include_structures=True,
            include_mechanics=True,
        )
        if frames and state != native.chemical_states.reference_chemical_state_index:
            raise ArgumentConflictError(
                "structures",
                "chemical_states",
                reason="Model construction requires the declared reference chemical state.",
                caller=caller,
            )
        parts[i] = native
        return (
            (parts if isinstance(source, (list, tuple)) else native),
            ([0] if frames else "all"),
            frames,
        )
    if frames and has_attribute(source, "n_chemical_states"):
        reference = get(source, reference_chemical_state_index=True)
        states = get(
            source, structure_indices=frames, structure_chemical_state_index=True
        )
        if any(not isinstance(v, (int, np.integer)) or v != reference for v in states):
            raise ArgumentConflictError(
                "structures",
                "chemical_states",
                reason="Model construction requires structures associated with the reference chemical state.",
                caller=caller,
            )
    return source, (frames if frames else "all"), frames


def make_recipe(molecular_system, structure_indices, engine):
    from molsysmt._private.smonitor import ArgumentError, NotImplementedMethodError
    from molsysmt.basic import convert

    caller = "molsysmt.molecular_mechanics.get_model_recipe"
    if engine != "OpenMM":
        raise NotImplementedMethodError(method=engine, caller=caller)
    import numpy as np
    import openmm

    source_forms = forms(molecular_system)
    parameterized = PARAMETERIZED.intersection(source_forms)
    if parameterized:
        if structure_indices is not None:
            raise ArgumentError(
                "structure_indices", value=structure_indices, caller=caller
            )
        if len(source_forms) != 1:
            raise NotImplementedMethodError(
                method="composite parameterized model inspection", caller=caller
            )
        if source_forms[0] == "openmm.Context":
            system = molecular_system.getSystem()
        elif source_forms[0] == "openmm.Simulation":
            system = molecular_system.context.getSystem()
        else:
            system = molecular_system
        controls, resources, consumed = {}, [], []
        source_frames = []
        provenance = "provided_parameterized_model"
    else:
        reject_unsupported(molecular_system, caller=caller)
        source, scope, source_frames = model_context(
            molecular_system, structure_indices, caller
        )
        controls, defaults = requested(source)
        system = convert(
            source, to_form="openmm.System", structure_indices=scope, **defaults
        )
        from molsysmt.molecular_mechanics import get_engine_forcefield

        resources = get_engine_forcefield(
            controls["forcefield"]["value"],
            water_model=controls["water_model"]["value"],
            implicit_solvent=controls["implicit_solvent"]["value"],
            engine=engine,
        )
        consumed, provenance = list(SUPPORTED), "constructed_from_declared_controls"
    from molsysmt import __version__
    from molsysmt._private.scientific_attribution import executed_software_reference

    items = [executed_software_reference("openmm", openmm.__version__)]
    if provenance == "constructed_from_declared_controls" and controls[
        "implicit_solvent"
    ]["value"] in {"OBC1", "OBC2"}:
        from molsysmt._private.scientific_citations import ARTICLES

        article = deepcopy(ARTICLES["onufriev_2004"])
        items.append(
            dict(
                id="doi:" + article["doi"],
                type="article",
                **article,
                url="https://doi.org/" + article["doi"],
                roles=["scientific_criterion"],
            )
        )
    result = dict(
        schema="molsysmt.model_recipe@1",
        method="parameterized_model_inspection",
        requested=controls,
        consumed_controls=consumed,
        unsupported_controls=list(UNSUPPORTED),
        unsupported_legacy_annotations=["MolecularMechanics.formal_charge"],
        effective=inspect_system(system),
        provenance=provenance,
        source_structure_indices=np.asarray(source_frames, dtype=np.int64),
        resources=resources,
        software={"molsysmt": __version__, "openmm": openmm.__version__},
        attribution=dict(
            schema="molsysmt.scientific_attribution@1", target=caller, items=items
        ),
    )
    return result
