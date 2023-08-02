from molsysmt._private.exceptions import ArgumentError

def digest_exclusion_rules(exclusion_rules, caller=None):

    if exclusion_rules is None:
        return []
    elif isinstance(exclusion_rules, str):
        return [exclusion_rules]
    elif isinstance(exclusion_rules, tuple):
        return list(exclusion_rules)
    elif isinstance(exclusion_rules, list):
        return exclusion_rules

    raise ArgumentError('exclusion_rules', value=exclusion_rules, caller=caller, message=None)

