
def check_platforms():

    from simtk.openmm import Platform as _Platform

    for ii in range(_Platform.getNumPlatforms()):
        platform_name  = _Platform.getPlatform(ii).getName()
        platform       = _Platform.getPlatformByName(platform_name)
        platform_speed = platform.getSpeed()
        print('Plataforma {} con velocidad {}'.format(platform_name,platform_speed))
    del(platform_name, platform, platform_speed, _Platform)

