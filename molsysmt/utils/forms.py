
def digest(item, to_form=None):

    from molsysmt.multitool import _get_form

    if type(item) in [list,tuple]:
        form_in=[]
        for ii in item:
            form_in.append(_get_form(ii))
    else:
        form_in=_get_form(item)

    if to_form is not None:
        form_out=to_form
    else:
        form_out=form_in

    return form_in, form_out

