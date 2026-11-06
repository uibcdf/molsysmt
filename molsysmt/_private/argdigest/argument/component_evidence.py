from ._attribute_query import digest_query_flag


def digest_component_evidence(component_evidence, caller=None):
    return digest_query_flag("component_evidence", component_evidence, caller)
