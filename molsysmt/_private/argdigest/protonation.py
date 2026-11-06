"""Validate operation-specific protonation boundaries without global pH changes."""

from .argument.engine import digest_engine
from .argument.in_place import digest_in_place
from .argument.molecular_system import digest_molecular_system
from .argument.skip_digestion import digest_skip_digestion
from .atom_expectations import _ph

DIGEST_OPTIONS = {
    "digestion_source": "molsysmt._private.argdigest.protonation",
    "digestion_style": "registry",
    "strictness": "error",
}

ARGUMENT_DIGESTERS = {
    "molecular_system": digest_molecular_system,
    "pH": _ph,
    "engine": digest_engine,
    "in_place": digest_in_place,
    "skip_digestion": digest_skip_digestion,
}
