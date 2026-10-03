"""Lazy, optional Ackredit boundary for scientific attribution.

No import hooks, reminders, DOI enrichment or journal are enabled by MolSysMT.
Hosts and applications own those choices. Bibliographic result metadata does
not depend on Ackredit being installed.
Catalog diagnostics remain emitted under strict warning filters; their own
promotion cannot replace completed results or scientific exceptions.
"""

from contextlib import contextmanager
from copy import deepcopy

from depdigest import dep_digest, is_installed


def _failed(operation, error):
    from molsysmt._private.smonitor.emitter import warn
    from molsysmt._private.smonitor.warnings import AckreditTrackingWarning

    diagnostic = AckreditTrackingWarning(
        extra={"operation": operation, "reason": f"{type(error).__name__}: {error}"}
    )
    try:
        warn(diagnostic)
    except AckreditTrackingWarning as promoted:
        # SMonitor emits the catalog event before applying Python's warning
        # filter. Optional attribution cannot replace science under an error
        # filter; only this diagnostic's promotion is isolated here.
        if promoted is not diagnostic:
            raise


@dep_digest("ackredit")
def _load_backend():
    import ackredit

    return ackredit


def backend():
    """Return the optional provider only when attribution is requested."""
    return _load_backend() if is_installed("ackredit") else None


@contextmanager
def scope(target):
    """Isolate provider failures from the scientific function's exceptions."""
    context = None
    try:
        provider = backend()
        if provider is not None:
            context = provider.scope(target)
            context.__enter__()
    except Exception as error:
        _failed("start attribution tracking", error)
        context, provider = None, None
    try:
        yield provider
    finally:
        if context is not None:
            import sys

            try:
                context.__exit__(*sys.exc_info())
            except Exception as error:
                _failed("finish attribution tracking", error)


def credit(ackredit, items, target):
    """Register detached bibliographic records and credit the reached branch."""
    if ackredit is None:
        return
    try:
        for item in items:
            record = deepcopy(
                {key: value for key, value in item.items() if key != "roles"}
            )
            ackredit.register_item(**record)
            ackredit.track_item(record["id"], used_by=target)
    except Exception as error:
        _failed("record scientific references", error)
