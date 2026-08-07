from molsysmt._private.smonitor import ArgumentError

def digest_platform(platform, caller=None):

    if isinstance(platform, str):
        if platform in ['CUDA', 'CPU']:
            return platform

    raise ArgumentError('platform', value=platform, caller=caller, message=None)

