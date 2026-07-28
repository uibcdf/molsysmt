"""
molsysmt.core
The low-level native engine of MolSysMT.

Exposes Rust-backed kernels to sister libraries such as TopoMT with no
high-level molecular-system or physical-unit overhead.
"""

import importlib

_LAZY_ATTRIBUTES = {
    "math": "molsysmt.lib.math",
    "pbc": "molsysmt.lib.pbc",
    "structure": "molsysmt.lib.structure",
    "topology": "molsysmt.lib.topology",
    "series": "molsysmt.lib.series",
}


def __getattr__(name: str):
    if name in _LAZY_ATTRIBUTES:
        target = _LAZY_ATTRIBUTES[name]
        mod = importlib.import_module(target)
        globals()[name] = mod
        return mod
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(list(globals().keys()) + list(_LAZY_ATTRIBUTES.keys()))


__all__ = []
