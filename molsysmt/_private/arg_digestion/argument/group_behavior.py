from ...exceptions import ArgumentError

def digest_group_behavior(group_behavior, caller=None):

    if group_behavior is None:
        return None

    elif isinstance(group_behavior, str):
        if group_behavior.lower() in ['center of mass', 'geometric center', 'closest', 'farthest']:
            return group_behavior.lower()

    raise ArgumentError('group_behavior', value=group_behavior, caller=caller, message=None)

