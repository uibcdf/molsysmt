from molsysmt._private.exceptions import ArgumentError

def digest_engine_sequence_alignment(engine_sequence_alignment, caller=None):

    from molsysmt.supported.engines import lowercase_engines

    if isinstance(engine_sequence_alignment, str):
        try:
            return lowercase_engines[engine_sequence_alignment.lower()]
        except:
            pass

    raise ArgumentError('engine_sequence_alignment', value=engine_sequence_alignment, caller=caller, message=None)

