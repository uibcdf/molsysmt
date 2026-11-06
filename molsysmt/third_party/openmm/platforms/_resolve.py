"""Resolve explicit OpenMM platform requests without selecting a substitute."""

from depdigest import dep_digest

from molsysmt._private.smonitor import (
    ArgumentChoiceError,
    ArgumentError,
    ExecutionPlatformUnavailableError,
)

# Vocabulary is engine-owned; installed third-party plugins are admitted too.
KNOWN_PLATFORMS = frozenset({"Reference", "CPU", "CUDA", "OpenCL", "HIP", "Metal"})


@dep_digest("openmm")
def resolve_platform(platform, caller):
    """Return the named registered platform, preserving later device failures."""
    from openmm import Platform

    from .platforms import available_platforms

    if isinstance(platform, Platform):
        return platform
    if not isinstance(platform, str) or not platform.strip():
        raise ArgumentError("platform", value=platform, caller=caller)
    registered = available_platforms(verbose=False)
    if platform not in registered:
        if platform not in KNOWN_PLATFORMS:
            raise ArgumentChoiceError(
                "platform",
                platform,
                sorted(KNOWN_PLATFORMS | set(registered)),
                caller=caller,
            )
        raise ExecutionPlatformUnavailableError(
            "OpenMM", platform, registered, caller=caller
        )
    return Platform.getPlatformByName(platform)
