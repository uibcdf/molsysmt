from ...exceptions import ArgumentError
from ...variables import is_all

def digest_bioassembly_index(bioassembly_index, caller=None):

    if caller.startswith('molsysmt.item.mmtf_MMTFDecoder.to_'):
        if isinstance(bioassembly_index, int):
            return bioassembly_index

    raise ArgumentError('bioassembly_index', value=bioassembly_index, caller=caller, message=None)

