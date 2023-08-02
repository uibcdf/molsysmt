from molsysmt._private.exceptions import ArgumentError

def digest_default_inclusion_rules(default_inclusion_rules, caller=None):

    if isinstance(default_inclusion_rules, bool):
        return default_inclusion_rules

    raise ArgumentError('default_inclusion_rules', value=default_inclusion_rules, caller=caller, message=None)

