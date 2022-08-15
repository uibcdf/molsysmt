from ...exceptions import ArgumentError

def digest_group_behavior_2(group_behavior_2, caller=None):

    if group_behavior_2 is None:
        return None

    from .group_behavior import digest_group_behavior

    try:
        return digest_group_behavior(group_behavior_2, caller=caller)
    except:
        raise ArgumentError('group_behavior_2', value=group_behavior_2, caller=caller, message=None)

