"""View binding and the explicitly admitted scientific module hierarchy."""

from weakref import ref

from ._basic import _BasicTools


class _MolSysMTTools:
    def __init__(self, view):
        self._view_ref = ref(view)
        self.basic = _BasicTools(self)

    def _target(self):
        view = self._view_ref()
        if view is None or view.closed:
            raise RuntimeError("MolSysMT tools cannot operate on a closed view.")
        target = view.molsys
        if target is None:
            raise ValueError("Load a molecular system before using this MolSysMT tool.")
        return target

    def __getattr__(self, name):
        # Keep root scientific aliases consistent with the admitted module API.
        if name in _BasicTools._NAMES:
            return getattr(self.basic, name)
        raise AttributeError(name)

    def __dir__(self):
        return ["basic", *_BasicTools._NAMES]
