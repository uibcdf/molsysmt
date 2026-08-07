from molsysmt._private.smonitor import ArgumentError


def digest_attribute_policy(attribute_policy, caller=None):
    """Validate the policy used for one-sided structural attributes."""

    if attribute_policy in {'intersection', 'strict'}:
        return attribute_policy
    raise ArgumentError(
        'attribute_policy',
        value=attribute_policy,
        caller=caller,
        message=None,
    )
