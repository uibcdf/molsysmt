"""Resolve and scope selected chemistry independently of its storage form."""

from contextlib import contextmanager
from contextvars import ContextVar

import numpy as np

from molsysmt._private.smonitor import StructuralInconsistencyError

_ACTIVE = ContextVar("molsysmt_active_chemical_state_indices", default={})


def resolve_index(count, reference, index, caller):
    """Validate a state position without creating a state or choosing an arbitrary one."""
    if not count:
        reason = "The collection has no chemical state; chemical data are unavailable."
    else:
        if index is None:
            index = reference
        if index is None:
            reason = f"The collection has {count} chemical states and no reference state; state-dependent access is ambiguous."
        elif isinstance(index, (bool, np.bool_)) or not isinstance(
            index, (int, np.integer)
        ):
            reason = "Chemical-state index must be an integer."
        elif not 0 <= int(index) < count:
            reason = f"Chemical-state index {index} is invalid for {count} states."
        else:
            return int(index)
    raise StructuralInconsistencyError(reason=reason, caller=caller)


def active_index(owner, index=None):
    """Prefer an explicit request over the context-local state position."""
    return _ACTIVE.get().get(id(owner)) if index is None else index


@contextmanager
def using_state(owner, index):
    """Scope provider access and restore nested/concurrent callers on every exit."""
    index = owner._resolve_index(index)
    token = _ACTIVE.set({**_ACTIVE.get(), id(owner): index})
    try:
        yield owner
    finally:
        _ACTIVE.reset(token)
