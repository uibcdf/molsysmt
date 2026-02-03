from molsysmt._private.exceptions import ArgumentError

def digest_from_item(from_item, form=None, caller=None):

    from molsysmt.basic import get_form

    try:
        in_form = get_form(from_item)
        output = True
    except:
        output = False

    if output:
        if form is not None:
            if in_form!=form:
                raise ArgumentError('item', value=item, caller=caller, message=None)
        return from_item

    raise ArgumentError('from_item', value=from_item, caller=caller, message=None)
