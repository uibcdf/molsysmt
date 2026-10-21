"""Copying resident state; domain owners supply their own lifecycle rules."""

from copy import deepcopy
from types import MappingProxyType

import numpy as np


def _slots(source):
    """Read extension slots without invoking constructors or storage properties."""
    values = {}
    for cls in type(source).__mro__:
        names = cls.__dict__.get("__slots__", ())
        if isinstance(names, str):
            names = (names,)
        for name in names:
            if name in {"__dict__", "__weakref__"}:
                continue
            if name.startswith("__") and not name.endswith("__"):
                name = f"_{cls.__name__.lstrip('_')}{name}"
            try:
                values[name] = getattr(source, name)
            except AttributeError:
                pass
    return values


def _prepare(value, memo, seen, proxies):
    """Seed proven immutable buffers and proxy shells in the standard copy memo."""
    identity = id(value)
    if identity in seen:
        return
    seen.add(identity)
    if type(value) is np.ndarray and not value.dtype.hasobject:
        owner = value
        while isinstance(owner, np.ndarray):
            owner = owner.base
        if isinstance(owner, bytes):
            # A read-only flag alone is insufficient: a caller may retain a
            # writable alias. A separate header also isolates shape changes.
            if identity in memo:
                replacement = memo[identity]
                while isinstance(replacement, np.ndarray):
                    replacement = replacement.base
                if not isinstance(replacement, bytes):
                    raise TypeError(
                        "The copy memo already replaces immutable native storage "
                        "with a mutable buffer; copy the owning object before its raw arrays"
                    )
            else:
                memo[identity] = value.view()
    elif identity in memo:
        return
    elif isinstance(value, MappingProxyType):
        contents = dict(value)
        target = {}
        memo[identity] = MappingProxyType(target)
        proxies.append((contents, target))
        _prepare(contents, memo, seen, proxies)
    elif isinstance(value, dict):
        for key, item in value.items():
            _prepare(key, memo, seen, proxies)
            _prepare(item, memo, seen, proxies)
    elif isinstance(value, (tuple, list, set, frozenset)):
        for item in value:
            _prepare(item, memo, seen, proxies)


def _clone(source, memo):
    """Detach mutable state while retaining immutable bytes and lazy graph shape."""
    if id(source) in memo:
        return memo[id(source)]
    result = object.__new__(type(source))
    memo[id(source)] = result
    state = (vars(source), _slots(source))
    proxies = []
    _prepare(state, memo, set(), proxies)
    attributes, slots = deepcopy(state, memo)
    result.__dict__.update(attributes)
    for name, value in slots.items():
        object.__setattr__(result, name, value)
    for contents, target in proxies:
        target.update(deepcopy(contents, memo))
    return result
