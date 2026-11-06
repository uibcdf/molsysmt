from ._attribute_query import digest_query_flag


def digest_component_completeness(component_completeness, caller=None):
    return digest_query_flag("component_completeness", component_completeness, caller)
