from molsysmt._private.smonitor import ArgumentError


def digest_use_gpu(use_gpu, caller=None):

    if use_gpu is None:
        return None

    if isinstance(use_gpu, bool):
        return use_gpu

    if isinstance(use_gpu, str) and use_gpu.lower() == 'auto':
        return 'auto'

    raise ArgumentError('use_gpu', value=use_gpu, caller=caller, message=None)
