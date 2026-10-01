"""Analyzing chemically interpreted interactions in molecular systems."""

from importlib import import_module

__all__ = ["hbonds", "disulfides", "ionic", "pi_pi", "cation_pi", "halogen_bonds", "hydrophobic", "metal_coordination", "water_bridges"]


def __getattr__(name):
    if name in __all__:
        module = import_module(f".{name}", __name__)
        globals()[name] = module
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(set(globals()) | set(__all__))
