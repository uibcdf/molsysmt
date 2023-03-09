# If digest is used in this method, other methods become slower

def where_is_attribute(molecular_system, attribute):

    from . import get_form
    from molsysmt.form import _dict_modules

    if not isinstance(molecular_system, (list, tuple)):
        molecular_system = [molecular_system]

    forms_in = get_form(molecular_system)

    where_form=[]
    where_item=[]

    for form_in, item in zip(forms_in, molecular_system):
        if _dict_modules[form_in].has_attribute(item, attribute):
            where_form.append(form_in)
            where_item.append(item)

    if len(where_form)==1:
        output_item = where_item[0]
        output_form = where_form[0]
    elif len(where_form)==0:
        output_item = None
        output_form = None
    else:
        print('This to correct in where_is_attribute')

    return output_item, output_form

