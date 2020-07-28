
def digest(item, to_form=None):

    from molsysmt.multitool import get_form

    if type(item) in [list,tuple]:
        form_in=[]
        for ii in item:
            form_in.append(get_form(ii))
    else:
        form_in=get_form(item)

    if to_form is not None:
        form_out=to_form
    else:
        form_out=form_in

    return form_in, form_out

