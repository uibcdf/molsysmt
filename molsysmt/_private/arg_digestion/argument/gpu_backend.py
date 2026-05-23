from molsysmt._private.smonitor import ArgumentError


def digest_gpu_backend(gpu_backend, caller=None):

    if gpu_backend is None:
        return None

    if isinstance(gpu_backend, str) and gpu_backend.lower() in ['cuda', 'taichi']:
        return gpu_backend.lower()

    raise ArgumentError('gpu_backend', value=gpu_backend, caller=caller, message=None)
