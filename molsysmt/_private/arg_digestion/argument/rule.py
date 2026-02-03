from molsysmt._private.exceptions import ArgumentError

def digest_rule(rule, caller=None):


    if caller == 'molsysmt.basic.compare.compare':

        if rule in ['equal', 'in']:
            return rule

    raise ArgumentError('rule', value=rule, caller=caller, message=None)
