"""View binding and the explicitly admitted scientific module hierarchy."""

from weakref import ref

from argdigest import arg_digest
from smonitor import signal

from ._basic import _BasicTools


class _MolSysMTTools:
    def __init__(self, view):
        self._view_ref = ref(view)
        self.basic = _BasicTools(self)

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
        return ["basic", "get_sync_status", "sync_view", *_BasicTools._NAMES]
