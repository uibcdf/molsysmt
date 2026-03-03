def is_form(item):

    output = False

    class_name = str(type(item))
    if 'MDAnalysis.core.groups.AtomGroup' in class_name:
        output = True

    return output
