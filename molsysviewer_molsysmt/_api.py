"""View binding and the explicitly admitted scientific module hierarchy."""

from weakref import ref

from argdigest import arg_digest
from smonitor import signal

from ._basic import _BasicTools
from ._build import _BuildTools
from ._interactions import _InteractionsTools
from ._pbc import _PbcTools
from ._physchem import _PhyschemTools
from ._structure import _StructureTools
from ._topology import _TopologyTools


class _MolSysMTTools:
    def __init__(self, view):
        self._view_ref = ref(view)
        self.basic = _BasicTools(self)
        self.build = _BuildTools(self)
        self.interactions = _InteractionsTools(self)
        self.topology = _TopologyTools(self)
        self.structure = _StructureTools(self)
        self.pbc = _PbcTools(self)
        self.physchem = _PhyschemTools(self)

    def _view(self):
        view = self._view_ref()
        if view is None or view.closed:
            raise RuntimeError("MolSysMT tools cannot operate on a closed view.")
        return view

    def _target(self):
        target = self._view().molsys
        if target is None:
            raise ValueError("Load a molecular system before using this MolSysMT tool.")
        return target

    def _read(self, function, parameters, extra=None):
        """Delegate one admitted primary-bound reader without copying its data."""
        if extra and "molecular_system" in extra:
            raise TypeError(
                "The primary molecular_system is bound to view.molsys and cannot be overridden."
            )
        view = self._view()
        self._target()
        coordinator = getattr(view.addons.manager, "system_edits", None)

        def call(target):
            return function(target, **parameters, **(extra or {}))

        if coordinator is not None:
            return coordinator.read(call)
        return call(self._target())

    @signal(tags=["addon", "edit"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_sync_status(self, *, skip_digestion=False):
        """Return detached managed-edit status; raw external edits are unobserved."""
        view = self._view_ref()
        if view is None:
            raise RuntimeError("The owning view no longer exists.")
        return view.addons.manager.system_edits.get_status(
            skip_digestion=skip_digestion
        )

    @signal(tags=["addon", "edit"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def sync_view(self, *, skip_digestion=False):
        """Retry pending scene reconciliation without repeating scientific work."""
        view = self._view_ref()
        if view is None:
            raise RuntimeError("The owning view no longer exists.")
        return view.addons.manager.system_edits.synchronize(
            skip_digestion=skip_digestion
        )

    def __getattr__(self, name):
        # Keep root scientific aliases consistent with the admitted module API.
        if name in _BasicTools._NAMES:
            return getattr(self.basic, name)
        raise AttributeError(name)

    def __dir__(self):
        return [
            "basic",
            "build",
            "interactions",
            "topology",
            "structure",
            "pbc",
            "physchem",
            "get_sync_status",
            "sync_view",
            *_BasicTools._NAMES,
        ]
