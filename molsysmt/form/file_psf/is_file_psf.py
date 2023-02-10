def is_file_psf(item):

    output = False

    if type(item)==str:
        if item.endswith('.psf'):
            output = True

    return output

