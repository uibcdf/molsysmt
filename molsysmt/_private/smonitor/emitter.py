try:
    from smonitor.integrations import DiagnosticBundle, emit_from_catalog, _catalog_entry, merge_extra
except ImportError:
    from smonitor.integrations import DiagnosticBundle, emit_from_catalog, merge_extra
    def _catalog_entry(catalog, level, key):
        section = catalog.get(level, {})
        return section.get(key)

from . import CATALOG, META, PACKAGE_ROOT

bundle = DiagnosticBundle(CATALOG, META, PACKAGE_ROOT)

warn = bundle.warn
warn_once = bundle.warn_once
resolve = bundle.resolve
experimental = bundle.experimental
support_tier = bundle.support_tier

def info(key, extra=None):
    entry = _catalog_entry(CATALOG, "info", key)
    if entry:
        emit_from_catalog(
            entry,
            package_root=PACKAGE_ROOT,
            extra=merge_extra(META, extra),
            meta=META,
        )

def debug(key, extra=None):
    entry = _catalog_entry(CATALOG, "debug", key)
    if entry:
        emit_from_catalog(
            entry,
            package_root=PACKAGE_ROOT,
            extra=merge_extra(META, extra),
            meta=META,
        )

# For backward compatibility within molsysmt refactoring
def message_from_catalog(entry, extra=None, default_message=None):
    return bundle.resolve(message=default_message, code=entry.get('code'), extra=extra)
