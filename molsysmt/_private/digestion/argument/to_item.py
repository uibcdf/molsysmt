from molsysmt._private.exceptions import ArgumentError

def digest_to_item(to_item, form=None, caller=None):

    from molsysmt.basic import get_form

    try:
        in_form = get_form(to_item)
        output = True
    except:
        output = False

    if output:
        if form is not None:
            if in_form!=form:
                raise ArgumentError('item', value=item, caller=caller, message=None)
        return to_item

    raise ArgumentError('to_item', value=to_item, caller=caller, message=None)
