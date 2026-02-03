from molsysmt._private.exceptions import ArgumentError

def digest_inclusion_rules(inclusion_rules, caller=None):

    if inclusion_rules is None:
        return []
    elif isinstance(inclusion_rules, str):
        return [inclusion_rules]
    elif isinstance(inclusion_rules, tuple):
        return list(inclusion_rules)
    elif isinstance(inclusion_rules, list):
        return inclusion_rules

    raise ArgumentError('inclusion_rules', value=inclusion_rules, caller=caller, message=None)

