from molsysmt._private.smonitor import ArgumentError

def digest_alignment_index(alignment_index, caller=None):

    from .index import arg_digest_index

    try:
        return digest_index(alignment_index, caller=caller)
    except:
        raise ArgumentError('alignment_index', value=alignment_index, caller=caller, message=None)

