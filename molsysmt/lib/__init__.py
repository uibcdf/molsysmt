import importlib

_LAZY_ATTRIBUTES = {
    'math': '.math',
    'series': '.series',
    'pbc': '.pbc',
    'structure': '.structure',
    'topology': '.topology',
}


def __getattr__(name: str):
    if name in _LAZY_ATTRIBUTES:
        target = _LAZY_ATTRIBUTES[name]
        mod = importlib.import_module(target, __name__)
        globals()[name] = mod
        return mod
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(list(globals().keys()) + list(_LAZY_ATTRIBUTES.keys()))


__all__ = []
