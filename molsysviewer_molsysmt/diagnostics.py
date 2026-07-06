"""Panel diagnostics for the MolSysMT MolSysViewer addon."""

from __future__ import annotations

from typing import Any


def compact_error_message(exc: Exception) -> str:
    """Return a short user-facing error message without traceback details."""
    if isinstance(exc, (ImportError, ModuleNotFoundError)):
        return "Missing optional dependency required for this operation."
    message = str(exc).strip().splitlines()[0] if str(exc).strip() else exc.__class__.__name__
    if len(message) > 160:
        message = f"{message[:157]}..."
    return message


def emit_panel_exception(
    view: Any,
    *,
    panel: str,
    action: str,
    exc: Exception,
) -> None:
    """Emit an SMonitor diagnostic for a panel failure.

    Uses the canonical ``context_extra`` schema so addon-panel failures triage
    identically to core viewer / MolSysMT failures. Emission is best-effort, but
    it is *not* silently swallowed: if SMonitor is installed and emission still
    fails, a ``RuntimeWarning`` is raised (honoring the "No Silent Emission
    Failures" directive). The local addon event log is always updated afterwards.
    """
    # 1. Structured emission to SMonitor.
    try:
        from smonitor.integrations import context_extra, emit_from_catalog

        from molsysmt._private.smonitor import CATALOG, META, PACKAGE_ROOT

        entry_key = (
            "LibraryNotFoundError"
            if isinstance(exc, (ImportError, ModuleNotFoundError))
            else "InternalAlgorithmError"
        )
        entry = CATALOG["exceptions"][entry_key]
        emit_from_catalog(
            entry,
            package_root=PACKAGE_ROOT,
            meta=META,
            extra=context_extra(
                caller=f"molsysviewer_molsysmt.panels.{panel}.{action}",
                operation=action,
                failure_class="addon-panel-action",
                last_failure_reason=compact_error_message(exc),
                causal_chain=[exc.__class__.__name__],
                evidence={"expected": "calculation ok", "observed": exc.__class__.__name__},
            ),
        )
    except (ImportError, ModuleNotFoundError):
        pass  # SMonitor not installed; expected on light deployments.
    except Exception as err:  # SMonitor present but emission failed -> do not stay silent.
        import warnings

        warnings.warn(
            f"SMonitor integration failed to emit panel diagnostics: {err}",
            RuntimeWarning,
            stacklevel=2,
        )

    # 2. Preserve the addon's local event log for panel state (crucial).
    try:
        from .runtime import record_event

        record_event(
            view,
            "panel_error",
            panel=panel,
            action=action,
            exception_type=exc.__class__.__name__,
            reason=compact_error_message(exc),
        )
    except Exception:
        pass


def panel_error_state(
    view: Any,
    *,
    panel: str,
    action: str,
    exc: Exception,
) -> dict[str, str]:
    """Log a panel exception and return the state payload for the widget."""
    emit_panel_exception(view, panel=panel, action=action, exc=exc)
    return {"status": "error", "error": compact_error_message(exc)}
