def available_platforms(verbose=True):

    """Available platforms to run OpenMM integratos

    List of available platforms to run an OpenMM MD integrators.

    Parameters
    ----------
    verbose : bool, default=True.
        If True, the method prints out a message with a line corresponding to each available
        platorm. If False, the method returns the list of platform names.

    Examples
    --------

    >>> from molsysmt.thirds.openmm import available_platforms
    >>> available_platorms()
    Platform Reference with speed 1.0
    Platform CPU with speed 10.0
    Platform CUDA with speed 100.0
    Platform OpenCL with speed 50.0


    Notes
    -----

    This methods invokes the simtk.openmm methods to work with the class `Platform`. You can check
    the `section Platforms in the OpenMM User Guide web page
    <http://docs.openmm.org/7.1.0/userguide/application.html#platforms>`_ and the `OpenMM Python API
    documentation <http://docs.openmm.org/latest/api-python/generated/simtk.openmm.openmm.Platform.html#>`_.

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

    """Loading failures of platorms to run OpenMM integrators

    List of failures at the time of importing OpenMM regarding the platforms to run the
    integrators..

    Parameters
    ----------

    Examples
    --------

    >>> from molsysmt.thirds.openmm import loading_failures
    >>> loading_failures()
    ('Error loading library /home/diego/Myopt/Miniconda/miniconda3/envs/UIBCDF_lab_dev/lib/plugins/libOpenMMCUDA.so: libcufft.so.9.2: cannot open shared object file: No such file or directory', 'Error loading library /home/diego/Myopt/Miniconda/miniconda3/envs/UIBCDF_lab_dev/lib/plugins/libOpenMMRPMDCUDA.so: libOpenMMCUDA.so: cannot open shared object file: No such file or directory', 'Error loading library /home/diego/Myopt/Miniconda/miniconda3/envs/UIBCDF_lab_dev/lib/plugins/libOpenMMDrudeCUDA.so: libOpenMMCUDA.so: cannot open shared object file: No such file or directory', 'Error loading library /home/diego/Myopt/Miniconda/miniconda3/envs/UIBCDF_lab_dev/lib/plugins/libOpenMMAmoebaCUDA.so: libOpenMMCUDA.so: cannot open shared object file: No such file or directory', 'Error loading library /home/diego/Myopt/Miniconda/miniconda3/envs/UIBCDF_lab_dev/lib/plugins/libOpenMMCudaCompiler.so: libnvrtc.so.9.2: cannot open shared object file: No such file or directory')

    Notes
    -----

    This methods invokes the simtk.openmm methods to work with the class `Platform`. You can check
    the `section Platforms in the OpenMM User Guide web page
    <http://docs.openmm.org/7.1.0/userguide/application.html#platforms>`_ and the `OpenMM Python API
    documentation <http://docs.openmm.org/latest/api-python/generated/simtk.openmm.openmm.Platform.html#>`_.

    """

    from openmm import Platform
    print(Platform.getPluginLoadFailures())

