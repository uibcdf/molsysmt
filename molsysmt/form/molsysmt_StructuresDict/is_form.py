
def is_form(item):

    output = False

    if type(item) is dict:

        from molsysmt.native.structures_dict import structures_parameters

        keys = set(item.keys())
        output = (keys <= structures_parameters)

    return output

