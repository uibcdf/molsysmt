from molsysmt._private.exceptions import ArgumentError

def digest_rule(rule, caller=None):


    if caller == 'molsysmt.basic.compare.compare.compare':

        if rule in ['A_eq_B', 'A_neq_B', 'A_in_B', 'B_in_A']:
            return rule

    raise ArgumentError('rule', value=rule, caller=caller, message=None)
