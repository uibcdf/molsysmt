from ...exceptions import ArgumentError

def digest_with_templates(with_templates, caller=None):

    if isinstance(with_templates, bool):
        return with_templates

    raise ArgumentError('with_templates', value=with_templates, caller=caller, message=None)

