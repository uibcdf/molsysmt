from molsysmt._private.exceptions import ArgumentError

def digest_default_exclusion_rules(default_exclusion_rules, caller=None):

    if isinstance(default_exclusion_rules, bool):
        return default_exclusion_rules

    raise ArgumentError('default_exclusion_rules', value=default_exclusion_rules, caller=caller, message=None)

