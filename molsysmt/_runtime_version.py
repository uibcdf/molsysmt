"""Resolve the imported package's build version without executing build tools.

This bootstrap helper deliberately lives outside ``_private``: importing that
package initializes argument validation before the root version is available.
"""

from importlib import import_module, metadata
from pathlib import Path

UNKNOWN_VERSION = "0+unknown"


def resolve_version(package_file):
    """Prefer the package-local build stamp, then explicitly owning metadata.

    A version labels a build, not an authenticated source-tree fingerprint.
    In particular, editable source can change after its stamp was generated.
    No source-control process, network request or runtime build dependency is
    involved; the root initializer caches this decision in ``__version__``.
    """
    package_file = Path(package_file).resolve()
    name = f"{__package__}._version"
    try:
        stamp = import_module(name)
    except ModuleNotFoundError as error:
        if error.name != name:
            # A broken generated module must not be disguised as another build.
            raise
    else:
        origin = getattr(stamp, "__file__", None)
        version = getattr(stamp, "__version__", None)
        if (
            origin is not None
            and Path(origin).resolve().parent == package_file.parent
            and isinstance(version, str)
            and version.strip()
        ):
            return version
        return UNKNOWN_VERSION

    try:
        distribution = metadata.distribution("molsysmt")
        for entry in distribution.files or ():
            if str(entry).replace("\\", "/") != "molsysmt/__init__.py":
                continue
            if Path(distribution.locate_file(entry)).resolve() == package_file:
                version = distribution.version
                if isinstance(version, str) and version.strip():
                    return version
                break
    except (metadata.PackageNotFoundError, OSError, ValueError):
        # Missing/unreadable installation records cannot establish ownership.
        pass
    return UNKNOWN_VERSION
