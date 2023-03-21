def is_form(item):

    output = False

    if type(item)==str:
        if item.endswith('.psf'):
            output = True

    return output

