"""Selecting explicitly implemented H5MSM roots without guessing migrations."""

DEFAULT_WRITE_VERSION = "1.0"
MECHANICS_VERSIONS = frozenset({"0.6", "1.0"})
MODULAR_VERSIONS = MECHANICS_VERSIONS | {"0.5"}


def write_version(value):
    """Require an implemented write contract even for trusted delegation."""
    if not isinstance(value, str) or value not in MODULAR_VERSIONS:
        raise ValueError(
            "H5MSM writing requires format_version '0.5', '0.6', or '1.0'."
        )
    return value


def root_version(root):
    """Read the stored label; never interpret an absent label as a legacy root."""
    value = root.attrs.get("version")
    return value.decode() if isinstance(value, bytes) else value
