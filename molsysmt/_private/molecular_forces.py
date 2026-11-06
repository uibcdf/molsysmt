"""Read full-model engine forces through bounded coordinate blocks."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest.argument._correspondence_axes import flat_axis
from molsysmt._private.execution.reducer import Reducer
from molsysmt._private.smonitor import (
    ArgumentConflictError,
    ArgumentError,
    MemoryBudgetExceededError,
    NotImplementedMethodError,
    NotWithThisFormError,
    StructuralInconsistencyError,
    UnsupportedHeavyOperationError,
)
from molsysmt._private.variables import is_all

CALLER = "molsysmt.molecular_mechanics.get_forces"
FORCE_UNIT = "kJ/(mol*nm)"
_DEFAULTS = (
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
)
_UNSUPPORTED_REQUESTS = (
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


def _indices(value, size, argument, *, default_first=False):
    if value is None and default_first:
        value = np.array([0], dtype=np.int64)
    if is_all(value):
        return np.arange(size, dtype=np.int64)
    if not (
        isinstance(value, np.ndarray) and value.ndim == 1 and value.dtype == np.int64
    ):
        value = flat_axis(value, argument, CALLER)
    if value is None or np.any(value < 0) or np.any(value >= size):
        raise ArgumentError(argument, value=value, caller=CALLER)
    return value


def _atoms(source, selection, n_atoms, syntax):
    from molsysmt.basic import select

    if isinstance(selection, str):
        values = select(source, selection=selection, syntax=syntax, skip_digestion=True)
        return _indices(values, n_atoms, "selection")
    if isinstance(selection, np.ndarray) and selection.dtype.kind == "b":
        if selection.ndim != 1 or len(selection) != n_atoms:
            raise ArgumentError("selection", value=selection, caller=CALLER)
        return np.flatnonzero(selection)
    return _indices(selection, n_atoms, "selection")


def _budget(shape, n_atoms, n_selected):
    from molsysmt import configure

    output_bytes = int(np.prod(shape)) * 16
    per_structure = 256 * n_atoms + 64 * n_selected + 4096
    available = int(configure.max_ram_usage) - output_bytes
    if available < per_structure:
        raise MemoryBudgetExceededError(
            reason="Resident forces and one coordinate/engine-transfer block exceed the numerical budget.",
            predicted_bytes=output_bytes + per_structure,
            available_bytes=int(configure.max_ram_usage),
            caller=CALLER,
        )
    return available, per_structure


def _read(context, atoms, magnitude):
    from openmm import unit

    values = (
        context.getState(getForces=True)
        .getForces(asNumpy=True)
        .value_in_unit(unit.kilojoule_per_mole / unit.nanometer)
    )
    values = np.asarray(values, dtype=np.float64)[atoms]
    if not np.all(np.isfinite(values)):
        raise StructuralInconsistencyError(
            reason="The engine returned nonfinite potential forces.", caller=CALLER
        )
    return np.linalg.norm(values, axis=-1) if magnitude else values


class _ForceReducer(Reducer):
    def __init__(self, context, atoms, n_atoms, magnitude, *, model_box=False):
        self.context = context
        self.atoms = atoms
        self.n_atoms = n_atoms
        self.magnitude = magnitude
        self.model_box = model_box
        self.periodic = context.getSystem().usesPeriodicBoundaryConditions()

    def initialize(self, metadata):
        shape = (metadata["n_structures"], len(self.atoms))
        self.output = np.empty(
            shape if self.magnitude else (*shape, 3), dtype=np.float64
        )
        self.offset = 0

    def consume(self, chunk):
        from openmm import unit

        from molsysmt._private.pbc_validation import validate_box_array

        coordinates = chunk["coordinates"]
        if (
            coordinates is None
            or coordinates.ndim != 3
            or coordinates.shape[1:] != (self.n_atoms, 3)
            or not np.all(np.isfinite(coordinates))
        ):
            raise StructuralInconsistencyError(
                reason="Force coordinates must be finite and span the complete atom axis.",
                caller=CALLER,
            )
        boxes = chunk["box"]
        if self.periodic and not (boxes is None and self.model_box):
            boxes = validate_box_array(boxes, len(coordinates), caller=CALLER)
        for index, xyz in enumerate(coordinates):
            if self.periodic and boxes is not None:
                self.context.setPeriodicBoxVectors(*(boxes[index] * unit.nanometer))
            self.context.setPositions(xyz * unit.nanometer)
            self.output[self.offset] = _read(self.context, self.atoms, self.magnitude)
            self.offset += 1

    def finalize(self):
        if self.offset != len(self.output):
            raise StructuralInconsistencyError(
                reason="Not every requested force structure was evaluated.",
                caller=CALLER,
            )
        return self.output


def _check_reference_state(source, frames):
    from molsysmt.basic import get, has_attribute

    if not has_attribute(source, "n_chemical_states"):
        return
    reference = get(source, reference_chemical_state_index=True)
    states = get(source, structure_indices=frames, structure_chemical_state_index=True)
    if any(
        not isinstance(state, (int, np.integer)) or state != reference
        for state in states
    ):
        raise ArgumentConflictError(
            "structure_indices",
            "chemical_states",
            reason="Force construction requires structures associated with the reference chemical state; select or declare a compatible model explicitly.",
            caller=CALLER,
        )


def _construct(source, frames, platform, forms):
    from molsysmt.basic import convert, has_attribute
    from molsysmt.configure import default_attribute

    parameterized = "openmm.System" in forms
    if not parameterized:
        unsupported = [
            name for name in _UNSUPPORTED_REQUESTS if has_attribute(source, name)
        ]
        if unsupported:
            raise NotImplementedMethodError(
                method="get_forces",
                arguments=unsupported,
                caller=CALLER,
                message="The construction adapter cannot apply these stored mechanical overrides; supply an explicitly parameterized Context/Simulation.",
            )
    names = _DEFAULTS[8:] if parameterized else _DEFAULTS
    missing = {
        name: default_attribute[name]
        for name in names
        if not has_attribute(source, name)
    }
    return convert(
        source,
        to_form="openmm.Context",
        selection="all",
        structure_indices=[int(frames[0])],
        platform=platform,
        **missing,
    )


def _quantity(values, legacy):
    if legacy:
        values = values[0]
    return puw.standardize(puw.quantity(values, FORCE_UNIT))


def _credit():
    import openmm

    from molsysmt._private.scientific_attribution import credit_executed_software

    credit_executed_software(
        "openmm",
        openmm.__version__,
        CALLER,
        observable="potential_forces",
        environment="complete_model",
    )


def _project_modular(source, selection, structure_indices, syntax, *, parameterized):
    """Read declared chemistry and one model structure, without saved analyses."""
    from molsysmt._private.h5msm import modular_h5msm_dimensions
    from molsysmt.basic import has_attribute

    parts = list(source) if isinstance(source, (list, tuple)) else [source]
    candidates = [
        (index, part, dimensions)
        for index, part in enumerate(parts)
        if (dimensions := modular_h5msm_dimensions(part)) is not None
    ]
    if not candidates:
        return None
    if len(candidates) != 1 or any(
        has_attribute(part, "coordinates")
        for index, part in enumerate(parts)
        if index != candidates[0][0]
    ):
        raise NotImplementedMethodError(
            method="get_forces",
            arguments="competing modular coordinate sources",
            caller=CALLER,
            message="Compose competing structural sources into an explicitly aligned native MolSys before force evaluation.",
        )
    index, filename, (n_atoms, n_structures) = candidates[0]
    frames = _indices(
        structure_indices, n_structures, "structure_indices", default_first=True
    )
    if len(frames):
        _budget((0,), n_atoms, 0)
    if parameterized:
        from molsysmt.form._h5msm05_modular import (
            _identity_link,
            _link_key,
            read_modular_file,
        )
        from molsysmt.native import MolSys

        payload = read_modular_file(filename, layers={"topology", "associations"})
        topology = payload["topology"]
        if topology is not None:
            link = _identity_link("atom", "structures", "topology")
            observed = next(
                (
                    entry
                    for entry in payload["associations"] or []
                    if _link_key(entry) == _link_key(link)
                ),
                None,
            )
            if observed is None or not isinstance(observed["indices"], str):
                raise StructuralInconsistencyError(
                    reason="Force atom queries require a declared identity link between the structural and topology atom axes.",
                    caller=CALLER,
                )
        reference = None
    else:
        from molsysmt.form._h5msm05_modular import _read_calculation_chemistry

        model, state = _read_calculation_chemistry(
            filename,
            chemical_state="structure" if len(frames) else "reference",
            structure_indices=frames,
        )
        reference = model.chemical_states.reference_chemical_state_index
        if len(frames) and state != reference:
            raise ArgumentConflictError(
                "structure_indices",
                "chemical_states",
                reason="Selected structures must use the declared reference chemical state for force construction.",
                caller=CALLER,
            )
    import h5py

    from molsysmt.form._h5msm05_structures import read_independent_structures

    with h5py.File(filename, "r") as file:
        selected_structures = read_independent_structures(
            file,
            structure_indices=[int(frames[0])]
            if len(frames)
            else ([0] if n_structures else []),
        )
        if parameterized:
            model = MolSys._from_partial_domains(
                topology=topology, structures=selected_structures
            )
        else:
            model.structures = selected_structures
        # Match the ordinary selector's first stored structural context.
        # This second bounded read is needed only for a nontrivial query.
        if (
            len(frames)
            and frames[0] != 0
            and isinstance(selection, str)
            and not is_all(selection)
        ):
            model.structures = read_independent_structures(file, structure_indices=[0])
        parts[index] = model
        model_source = parts if isinstance(source, (list, tuple)) else model
        atoms = _atoms(model_source, selection, n_atoms, syntax)
        model.structures = selected_structures
    if reference is not None:
        model._set_structure_chemical_state_indices([reference] if n_structures else [])
    return model_source, filename, n_atoms, frames, atoms


def calculate(source, *, selection, structure_indices, magnitude, platform, syntax):
    from molsysmt import configure
    from molsysmt._private.execution import ChunkedExecutor
    from molsysmt.basic import get, get_form, has_attribute, where_is_attribute
    from molsysmt.form import _dict_modules

    form = get_form(source)
    forms = [form] if isinstance(form, str) else form
    legacy = structure_indices is None
    engine_forms = {"openmm.Context", "openmm.Simulation"}
    if isinstance(form, str) and form in engine_forms:
        context = source if form == "openmm.Context" else source.context
        n_atoms = context.getSystem().getNumParticles()
        atoms = _atoms(source, selection, n_atoms, syntax)
        frames = _indices(structure_indices, 1, "structure_indices", default_first=True)
        shape = (len(frames), len(atoms)) + (() if magnitude else (3,))
        if not len(frames) or not len(atoms):
            return _quantity(np.empty(shape), legacy)
        _budget(shape, n_atoms, len(atoms))
        values = np.repeat(_read(context, atoms, magnitude)[None], len(frames), axis=0)
        _credit()
        return _quantity(values, legacy)
    if any(item in engine_forms for item in forms):
        raise NotImplementedMethodError(
            method="get_forces",
            arguments="composite engine context",
            caller=CALLER,
            message="Supply an existing Context or Simulation directly, without a competing composite model.",
        )
    projection = _project_modular(
        source,
        selection,
        structure_indices,
        syntax,
        parameterized="openmm.System" in forms,
    )
    if projection is None:
        if not has_attribute(source, "coordinates"):
            raise NotWithThisFormError(
                form=form, requested_attribute="coordinates", caller=CALLER
            )
        n_atoms, n_structures = get(source, n_atoms=True, n_structures=True)
        atoms = _atoms(source, selection, n_atoms, syntax)
        frames = _indices(
            structure_indices, n_structures, "structure_indices", default_first=True
        )
        model_source = source
        coordinate_source, coordinate_form = where_is_attribute(source, "coordinates")
    else:
        model_source, coordinate_source, n_atoms, frames, atoms = projection
        coordinate_form = "file:h5msm"
    shape = (len(frames), len(atoms)) + (() if magnitude else (3,))
    if not len(frames) or not len(atoms):
        return _quantity(np.empty(shape), legacy)
    available, per_structure = _budget(shape, n_atoms, len(atoms))
    if projection is None and "openmm.System" not in forms:
        _check_reference_state(source, frames)
    context = _construct(
        model_source, frames if projection is None else np.array([0]), platform, forms
    )
    if context.getSystem().getNumParticles() != n_atoms:
        raise StructuralInconsistencyError(
            reason="The constructed particle axis differs from the source atom axis.",
            caller=CALLER,
        )
    reducer = _ForceReducer(
        context, atoms, n_atoms, magnitude, model_box="openmm.System" in forms
    )
    try:
        periodic = reducer.periodic
        box_source, _ = (
            where_is_attribute(source, "box")
            if periodic and projection is None
            else (coordinate_source, coordinate_form)
        )
        attributes = (
            ["coordinates", "box"]
            if periodic and has_attribute(model_source, "box")
            else ["coordinates"]
        )
        support = getattr(_dict_modules[coordinate_form], "_heavy_support", {})
        streamed = all(support.get(name, False) for name in attributes) and (
            not periodic or box_source is coordinate_source
        )
        if streamed:
            values = ChunkedExecutor(
                coordinate_source,
                coordinate_form,
                "get_forces",
                reducer=reducer,
                atom_indices="all",
                structure_indices=frames,
                attributes=attributes,
                heavy_mode="force" if len(frames) > 1 else "off",
                max_chunk_size=max(
                    1, min(configure.chunk_size, available // per_structure)
                ),
            ).execute()
        else:
            if projection is not None:
                raise UnsupportedHeavyOperationError(
                    operation="get_forces",
                    form=str(form),
                    reason="The modular coordinate source has no declared streaming route.",
                )
            if len(frames) * per_structure > available:
                raise UnsupportedHeavyOperationError(
                    operation="get_forces",
                    form=str(form),
                    reason="This coordinate/box composition has no declared bounded streaming route.",
                )
            coordinates = get(
                source, element="atom", structure_indices=frames, coordinates=True
            )
            box = (
                get(source, structure_indices=frames, box=True)
                if periodic and has_attribute(source, "box")
                else None
            )
            reducer.initialize({"n_structures": len(frames)})
            reducer.consume(
                ChunkedExecutor._build_chunk(
                    {
                        "coordinates": coordinates,
                        "box": box,
                        "structure_indices": frames,
                    }
                )
            )
            values = reducer.finalize()
    finally:
        reducer.context = None
        del context
    _credit()
    return _quantity(values, legacy)
