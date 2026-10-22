"""Copying resident state; domain owners supply their own lifecycle rules."""

from copy import deepcopy
from types import MappingProxyType, MemberDescriptorType

import numpy as np


def _copy_independently(source, skip_digestion):
    """Use the native deep-copy hook after checking the public delegation flag."""
    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(skip_digestion)
    return deepcopy(source)


def _deferred_geometry_memo(structures):
    """Seed independent handles for protected geometry in one native domain."""
    if structures is None:
        return {}
    return {
        id(value): value._fork()
        for value in (structures._coordinates, structures._box)
        if value is not None
    }


def _slots(source, *, exclude=(), qualified=False):
    """Read declared slot storage, retaining its owner when copying resident state."""
    values = {}
    declared = set()
    shadowed = set()
    for cls in type(source).__mro__:
        for name, descriptor in vars(cls).items():
            if (
                name in exclude
                or not isinstance(descriptor, MemberDescriptorType)
                or descriptor.__objclass__ is not cls
                or descriptor.__name__ != name
            ):
                continue
            if not qualified:
                if name in declared:
                    shadowed.add(name)
                declared.add(name)
            try:
                value = descriptor.__get__(source, type(source))
            except AttributeError:
                continue
            key = (cls, name) if qualified else name
            values[key] = value
    if not qualified:
        for name in sorted(shadowed):
            if name in values:
                raise TypeError(
                    f"Serialization cannot preserve repeated slot name {name!r}; "
                    "provide a subclass serialization hook"
                )
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


def _clone(source, memo, *, exclude=()):
    """Detach mutable state while retaining immutable bytes and lazy graph shape."""
    if id(source) in memo:
        return memo[id(source)]
    result = object.__new__(type(source))
    memo[id(source)] = result
    attributes = vars(source)
    if exclude:
        attributes = {
            key: value for key, value in attributes.items() if key not in exclude
        }
    state = (attributes, _slots(source, exclude=exclude, qualified=True))
    proxies = []
    _prepare(state, memo, set(), proxies)
    attributes, slots = deepcopy(state, memo)
    result.__dict__.update(attributes)
    for (cls, name), value in slots.items():
        vars(cls)[name].__set__(result, value)
    for contents, target in proxies:
        target.update(deepcopy(contents, memo))
    return result
