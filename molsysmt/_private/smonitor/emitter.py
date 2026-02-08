from __future__ import annotations

from smonitor.integrations import DiagnosticBundle
from . import CATALOG, META, PACKAGE_ROOT

bundle = DiagnosticBundle(CATALOG, META, PACKAGE_ROOT)

warn = bundle.warn
warn_once = bundle.warn_once
resolve = bundle.resolve

# For backward compatibility within molsysmt refactoring
def message_from_catalog(entry, extra=None, default_message=None):
    return bundle.resolve(message=default_message, code=entry.get('code'), extra=extra)