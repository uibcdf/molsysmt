"""Explicit force-field metadata and primary-bound mechanical degree counting."""

from argdigest import arg_digest
from smonitor import signal

from ._basic import _native_documentation


def _mechanical_documentation(name, *, bind_primary):
    def decorate(function):
        function = _native_documentation(
            name, module="molecular_mechanics", bind_primary=bind_primary
        )(function)
        function.__doc__ += "\nView integration\n----------------\n"
        if bind_primary:
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
                "ownership remain unchanged. Native resource lists can be "
                "shared; make an explicit copy before customizing a list.\n"
            )
        return function

    return decorate


class _MolecularMechanicsTools:
    _NAMES = ("get_engine_forcefield", "get_degrees_of_freedom")

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
