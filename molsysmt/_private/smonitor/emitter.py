from __future__ import annotations

from smonitor.integrations import DiagnosticBundle, emit_from_catalog
from . import CATALOG, META, PACKAGE_ROOT

bundle = DiagnosticBundle(CATALOG, META, PACKAGE_ROOT)

warn = bundle.warn
warn_once = bundle.warn_once
resolve = bundle.resolve

def debug(key, extra=None):
    if key in CATALOG["debug"]:
        emit_from_catalog(
            CATALOG["debug"][key],
            package_root=PACKAGE_ROOT,
            meta=META,
            extra=extra,
        )

# For backward compatibility within molsysmt refactoring
def message_from_catalog(entry, extra=None, default_message=None):
    return bundle.resolve(message=default_message, code=entry.get('code'), extra=extra)
