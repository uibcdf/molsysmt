from molsysmt._private.exceptions import ArgumentError

def digest_engine_least_rmsd_fit(engine_least_rmsd_fit, caller=None):

    from molsysmt.engine.engines import lowercase_engines

    if isinstance(engine_least_rmsd_fit, str):
        try:
            return lowercase_engines[engine_least_rmsd_fit.lower()]
        except:
            pass

    raise ArgumentError('engine_least_rmsd_fit', value=engine_least_rmsd_fit, caller=caller, message=None)

