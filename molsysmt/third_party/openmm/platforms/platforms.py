from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest()
@dep_digest("openmm")
def available_platforms(verbose=True):
    """
    Listing registered OpenMM compute platforms on the host machine.


    Parameters
    ----------
    verbose : bool, default=True
        Print platform names and engine speed estimates. With False, return
        the names instead. Registry discovery does not initialize a device.

    Returns
    -------
    list of str or none
        Registered platform names when verbose=False; otherwise None after
        printing. Registration alone does not certify context/driver readiness.

    Examples
    --------
    >>> from molsysmt.third_party.openmm.platforms import available_platforms
    >>> names = available_platforms(verbose=False)
    >>> 'Reference' in names
    True

    .. versionadded:: 1.0.0
    """

    from openmm import Platform

    platforms_available = []

    for ii in range(Platform.getNumPlatforms()):
        platform_name = Platform.getPlatform(ii).getName()
        platform = Platform.getPlatformByName(platform_name)
        platform_speed = platform.getSpeed()
        platforms_available.append(platform_name)
        if verbose:
            print("Platform {} with speed {}".format(platform_name, platform_speed))
        del (platform_name, platform, platform_speed)

    if verbose is False:
        return platforms_available


@arg_digest()
@dep_digest("openmm")
def loading_failures():
    """
    Retrieving OpenMM platform plugin loading failure messages.


    Returns
    -------
    none
        Print the engine's platform-plugin loading failure messages. The
        existing print-only return contract is preserved.

    Examples
    --------
    >>> from contextlib import redirect_stdout
    >>> from io import StringIO
    >>> from molsysmt.third_party.openmm.platforms import loading_failures
    >>> with redirect_stdout(StringIO()):
    ...     result = loading_failures()
    >>> result is None
    True

    .. versionadded:: 1.0.0
    """

    from openmm import Platform

    print(Platform.getPluginLoadFailures())
