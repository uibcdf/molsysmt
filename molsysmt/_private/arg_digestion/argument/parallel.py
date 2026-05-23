from molsysmt._private.smonitor import ArgumentError

def digest_parallel(parallel, caller=None):
    if parallel is None:
        return None
    if isinstance(parallel, bool):
        return parallel
    if isinstance(parallel, str):
        pl = parallel.lower()
        if pl in {'true', 'yes', 'on'}:
            return True
        if pl in {'false', 'no', 'off'}:
            return False
        if pl == 'auto':
            return 'auto'

    raise ArgumentError('parallel', value=parallel, caller=caller, message='parallel must be True, False, "auto", or None')
