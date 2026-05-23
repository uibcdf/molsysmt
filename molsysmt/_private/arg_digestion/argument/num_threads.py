from molsysmt._private.smonitor import ArgumentError

def digest_num_threads(num_threads, caller=None):
    if num_threads is None:
        return None
    if isinstance(num_threads, int):
        if num_threads == -1 or num_threads > 0:
            return num_threads
    if isinstance(num_threads, str):
        try:
            val = int(num_threads)
            if val == -1 or val > 0:
                return val
        except ValueError:
            pass

    raise ArgumentError('num_threads', value=num_threads, caller=caller, message='num_threads must be -1, a positive integer, or None')
