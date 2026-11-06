"""Explicit force-field metadata and primary-bound mechanical calculations."""

from argdigest import arg_digest
from smonitor import signal

from ._basic import _native_documentation
from ._geometry import _run_geometry_transform


def _mechanical_documentation(name, *, bind_primary):
    def decorate(function):
        function = _native_documentation(
            name, module="molecular_mechanics", bind_primary=bind_primary
        )(function)
        function.__doc__ += "\nView integration\n----------------\n"
        if name == "potential_energy_minimization":
            function.__doc__ += (
                "update_view : bool, keyword-only, default=True\n"
                "    Reconcile an admitted in-place coordinate edit. False "
                "defers scene projection only; sync_view() completes pending "
                "work without repeating minimization. Native in_place=False "
                "returns an independent system without adoption, regardless "
                "of this flag.\n"
                "skip_digestion : bool, keyword-only, default=False\n"
                "    Control addon digestion only. The native minimizer has "
                "no declared escape hatch and always receives ordinary "
                "validation.\n"
                "Requires an open loaded owner and native OpenMM/model/chemical "
                "prerequisites. Native method, platform, defaults, units, "
                "to_form, verbose and return ownership remain unchanged. "
                "Only a single-structure CPU or Reference NoCutoff/HBonds route is qualified; "
                "there is no implicit visible-structure selection, trajectory "
                "loop, molecular preparation or engine fallback. Source atom "
                "and structure identities are retained. Named analyses follow "
                "native coordinate-write invalidation and are not recalculated. "
                "A scene synchronization failure exposes science_completed=True "
                "and the native scientific_result; retry synchronization, not "
                "scientific work. Uncertain scientific writes require explicit "
                "recovery. Minimization seeks a local minimum, without a global "
                "minimum or equilibrium-ensemble guarantee.\n"
            )
        elif name == "get_non_bonded_potential_energy":
            function.__doc__ += (
                "Reads the current view.molsys through the serialized molecular "
                "reader, including completed pending edits. Native stored/default "
                "mechanical settings parameterize the complete system. With "
                "selection_2=None the result is its selected internal nonbonded "
                "energy; two disjoint selections request their native cross "
                "contribution. Scientific receiving covers single-structure CPU or Reference "
                "NoCutoff models, explicit atomic selections and two-sided group "
                "partitions. Native units, syntax and result axes remain intact. "
                "Native #561 also admits mixed partition/flat axes, retaining "
                "a singleton matrix axis for the flat side. Cross axes must "
                "be disjoint; arbitrary periodic long-range partitioning is "
                "not scientifically qualified here. No force field, chemistry "
                "preparation, visible-structure choice, scene/history change or "
                "update_view control is introduced. Native errors propagate.\n"
            )
        elif name == "get_forces":
            function.__doc__ += (
                "Reads the complete current view.molsys through the serialized "
                "molecular reader, including completed pending edits. Atom "
                "selection filters the returned forces after full-model "
                "evaluation; it does not extract a physical subsystem. Native "
                "structure_indices=None reads the first structure without a "
                "structure axis, regardless of the visible structure. Explicit "
                "structure selections retain their axis, order and repetitions; "
                "atomic repetitions, empty axes and magnitude are native. "
                "Returns detached raw potential forces under the application's "
                "unit policy, not constraint reaction forces or accelerations. "
                "Stored model requests, reference-state requirements, periodic "
                "boxes, engine/platform errors and numerical memory limits "
                "remain native. No model, chemistry preparation, minimization, "
                "visible-structure choice, scene/history update, force arrows "
                "or update_view control is introduced. CPU/Reference model "
                "receiving remains distinct from optional GPU qualification.\n"
            )
        elif name == "get_potential_energy":
            function.__doc__ += (
                "Reads the current view.molsys through the serialized molecular "
                "reader, including completed pending edits. Requires an open "
                "loaded owner and native OpenMM parameterization prerequisites. "
                "The native stored/default mechanical settings determine the "
                "force field and nonbonded method; this facade does not prepare "
                "chemistry or assign mechanics. Selection constructs the native "
                "selected subsystem, not an energy contribution inside an "
                "otherwise unchanged environment. Results are native energy "
                "quantities, or a force-name dictionary when decomposition=True, "
                "under the application's unit policy. No visible-structure "
                "selection, scene/history update or update_view control is "
                "introduced. Explicit single-structure CPU and Reference calculations are "
                "qualified; native multiple-structure box, partial-subsystem "
                "parameterization limits remain. Platform names are resolved by the native engine; unavailable registration and device failures do not select a substitute. GPU execution is not qualified here. Native "
                "errors and optional-engine requirements propagate unchanged.\n"
            )
        elif bind_primary:
            function.__doc__ += (
                "Reads the current view.molsys through the serialized molecular "
                "reader, including completed pending edits. An open loaded "
                "owner is required. Native OpenMM conversion, force-field and "
                "chemical prerequisites apply; the addon does not add atoms, "
                "protonate or assign stored mechanics. There is no implicit "
                "visible-structure selection or update_view control, and no "
                "scene/history change. The native definition is three times "
                "the particle count minus the constraint count; it adds no "
                "center-of-mass or thermostat correction. Native conversion "
                "can reject multiple-structure boxes; use an explicitly "
                "selected single-structure view for the qualified route. "
                "Native failures and optional-engine requirements propagate.\n"
            )
        else:
            function.__doc__ += (
                "Works with an open empty view; no current molecular system "
                "is inserted. This is a native resource-name lookup (XML "
                "resources for OpenMM or leaprc resources for LEaP), not an "
                "engine construction, availability check or parameterization. "
                "It does not load the selected engine or synchronize pending "
                "edits. Native lookup errors, model precedence and result "
                "ownership remain native. Each resource lookup owns its list; "
                "editing it does not alter the registry or subsequent calls. "
                "OBC1 and OBC2 select distinct physical model resources.\n"
            )
        return function

    return decorate


class _MolecularMechanicsTools:
    _NAMES = (
        "get_engine_forcefield",
        "get_degrees_of_freedom",
        "get_forces",
        "get_potential_energy",
        "get_non_bonded_potential_energy",
        "potential_energy_minimization",
    )

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    @_mechanical_documentation("get_engine_forcefield", bind_primary=False)
    @signal(tags=["addon", "molecular_mechanics", "metadata"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_engine_forcefield(
        self,
        forcefield,
        implicit_solvent=None,
        water_model=None,
        engine="OpenMM",
        skip_digestion=False,
    ):
        from molsysmt.molecular_mechanics import get_engine_forcefield

        self._owner._view()
        return get_engine_forcefield(
            forcefield,
            implicit_solvent=implicit_solvent,
            water_model=water_model,
            engine=engine,
            skip_digestion=skip_digestion,
        )

    @_mechanical_documentation("get_degrees_of_freedom", bind_primary=True)
    @signal(tags=["addon", "molecular_mechanics", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_degrees_of_freedom(
        self,
        forcefield="AMBER14",
        water_model=None,
        implicit_solvent=None,
        skip_digestion=False,
    ):
        from molsysmt.molecular_mechanics import get_degrees_of_freedom

        return self._owner._read(
            get_degrees_of_freedom,
            {
                "forcefield": forcefield,
                "water_model": water_model,
                "implicit_solvent": implicit_solvent,
                "skip_digestion": skip_digestion,
            },
        )

    @_mechanical_documentation("get_forces", bind_primary=True)
    @signal(tags=["addon", "molecular_mechanics", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_forces(
        self,
        element="atom",
        selection="all",
        magnitude=False,
        engine="OpenMM",
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        structure_indices=None,
        platform="CPU",
    ):
        from molsysmt.molecular_mechanics import get_forces

        return self._owner._read(
            get_forces,
            {
                "element": element,
                "selection": selection,
                "magnitude": magnitude,
                "engine": engine,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
                "structure_indices": structure_indices,
                "platform": platform,
            },
        )

    @_mechanical_documentation("get_potential_energy", bind_primary=True)
    @signal(tags=["addon", "molecular_mechanics", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_potential_energy(
        self,
        selection="all",
        decomposition=False,
        platform="CPU",
        engine="OpenMM",
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        from molsysmt.molecular_mechanics import get_potential_energy

        return self._owner._read(
            get_potential_energy,
            {
                "selection": selection,
                "decomposition": decomposition,
                "platform": platform,
                "engine": engine,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_mechanical_documentation("get_non_bonded_potential_energy", bind_primary=True)
    @signal(tags=["addon", "molecular_mechanics", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_non_bonded_potential_energy(
        self,
        selection="all",
        selection_2=None,
        platform="CPU",
        engine="OpenMM",
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        from molsysmt.molecular_mechanics import get_non_bonded_potential_energy

        return self._owner._read(
            get_non_bonded_potential_energy,
            {
                "selection": selection,
                "selection_2": selection_2,
                "platform": platform,
                "engine": engine,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_mechanical_documentation("potential_energy_minimization", bind_primary=True)
    @signal(tags=["addon", "molecular_mechanics", "edit"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def potential_energy_minimization(
        self,
        method="L-BFGS",
        platform="CPU",
        engine="OpenMM",
        to_form=None,
        in_place=False,
        verbose=False,
        *,
        update_view=True,
        skip_digestion=False,
    ):
        return _run_geometry_transform(
            self._owner,
            "potential_energy_minimization",
            {
                "method": method,
                "platform": platform,
                "engine": engine,
                "to_form": to_form,
                "in_place": in_place,
                "verbose": verbose,
            },
            update_view,
            module="molecular_mechanics",
        )
