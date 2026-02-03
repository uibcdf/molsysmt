from ...exceptions import ArgumentError
from ...variables import is_all

def digest_mmtf_entity(mmtf_entity, caller=None):

    if isinstance(mmtf_entity, dict):
        return mmtf_entity

    raise ArgumentError('mmtf_entity', value=mmtf_entity, caller=caller, message=None)
