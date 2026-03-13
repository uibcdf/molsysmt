from __future__ import annotations

from smonitor.integrations import DiagnosticBundle, emit_from_catalog
from . import CATALOG, META, PACKAGE_ROOT

bundle = DiagnosticBundle(CATALOG, META, PACKAGE_ROOT)

warn = bundle.warn
warn_once = bundle.warn_once
resolve = bundle.resolve

def info(key, extra=None):
    if key in CATALOG["info"]:
        emit_from_catalog(
            CATALOG["info"][key],
            package_root=PACKAGE_ROOT,
            meta=META,
            extra=extra,
        )

def debug(key, extra=None):
    if key in CATALOG["debug"]:
        emit_from_catalog(
            CATALOG["debug"][key],
            package_root=PACKAGE_ROOT,
            meta=META,
            extra=extra,
        )

def experimental_module(module_name):
    def decorator(fn):
        from functools import wraps
        @wraps(fn)
        def wrapper(*args, **kwargs):
            info("ExperimentalModule", extra={"module": module_name})
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# For backward compatibility within molsysmt refactoring
def message_from_catalog(entry, extra=None, default_message=None):
    return bundle.resolve(message=default_message, code=entry.get('code'), extra=extra)
