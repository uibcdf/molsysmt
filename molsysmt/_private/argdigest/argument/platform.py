from molsysmt._private.smonitor import ArgumentError


def digest_platform(platform, caller=None):

    # Names and availability belong to the selected engine, not this boundary.
    if isinstance(platform, str) and platform.strip():
        return platform

    raise ArgumentError("platform", value=platform, caller=caller, message=None)
