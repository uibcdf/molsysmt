from molsysmt._private.smonitor import ArgumentError


def digest_comparison(comparison, rule, caller=None):

    if caller == 'molsysmt.basic.compare.compare.compare' and isinstance(comparison, str):
        comparison = comparison.lower()
        if rule == 'equal' and comparison == 'equal':
            return comparison
        if rule == 'in' and comparison == 'in':
            return comparison

    raise ArgumentError('comparison', value=comparison, caller=caller, message=None)
