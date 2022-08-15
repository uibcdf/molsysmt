from molsysmt._private.exceptions import ArgumentError

def digest_items(items, forms=None, caller=None):

    from molsysmt.basic import get_form

    aux_items = items

    if not isinstance(items, (list, tuple)):
        aux_items = [items]

    output_items = []
    in_forms = []
    output = True

    for item in aux_items:
        try:
            in_forms.append(get_form(item))
        except:
            output = False
            break

    if output:
        if forms is not None:
            if isinstance(forms, str):
                forms = [forms]
            for in_form, form in zip(in_forms, forms):
                if in_form!=form:
                    message = "The items have not the required forms."
                    raise ArgumentError('item', value=item, caller=caller, message=None)
        return aux_items

    raise ArgumentError('items', value=items, caller=caller, message=None)
