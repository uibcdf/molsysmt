from ...exceptions import ArgumentError

def digest_prettyprint(prettyprint, caller=None):

    if caller=='molsysmt.topology.get_sequence_alignment.get_sequence_alignment':
        if isinstance(prettyprint, bool):
            return prettyprint

    raise ArgumentError('prettyprint', value=prettyprint, caller=caller, message=None)

