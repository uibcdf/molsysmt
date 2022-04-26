def selection_is_all(selection):

    output = False
    if type(selection) is str:
        trimmed = selection.replace(' ','')
        if trimmed.lower()=='all':
            output = True

    return output


