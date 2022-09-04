from ...exceptions import ArgumentError
from ...variables import is_all

def digest_bioassembly_name(bioassembly_name, caller=None):

    if bioassembly_name is None:
        return None

    if isinstance(bioassembly_name, str):
        return bioassembly_name

    raise ArgumentError('bioassembly_name', value=bioassembly_name, caller=caller, message=None)

