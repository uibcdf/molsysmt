def available_platforms(verbose=True):

    """
    Listing available OpenMM compute platform backend names on the host machine.


    Parameters
    ----------
    verbose : object, default=True
        Argument verbose.

    Returns
    -------
    list of str
        List of available platform names (e.g. `['Reference', 'CPU', 'CUDA', 'OpenCL']`).


    .. versionadded:: 1.0.0
    """


    from openmm import Platform

    platforms_available = []

    for ii in range(Platform.getNumPlatforms()):
        platform_name  = Platform.getPlatform(ii).getName()
        platform       = Platform.getPlatformByName(platform_name)
        platform_speed = platform.getSpeed()
        platforms_available.append(platform_name)
        if verbose:
            print('Platform {} with speed {}'.format(platform_name,platform_speed))
        del(platform_name, platform, platform_speed)

    if verbose is False:
        return platforms_available

def loading_failures():

    """
    Retrieving OpenMM platform plugin loading failure messages.


    Returns
    -------
    tuple of str
        Error strings reported when attempting to dynamically load platform plugins.


    .. versionadded:: 1.0.0
    """

    from openmm import Platform
    print(Platform.getPluginLoadFailures())

