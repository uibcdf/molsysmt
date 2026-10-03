from molsysmt._private.smonitor import ArgumentError


def digest_stereo_engine(stereo_engine, caller=None):
    """Validate explicit authorization for optional stereo interpretation."""
    if stereo_engine is None:
        return None
    if isinstance(stereo_engine, str) and stereo_engine.lower() == 'rdkit':
        return 'rdkit'
    raise ArgumentError('stereo_engine', value=stereo_engine, caller=caller)
