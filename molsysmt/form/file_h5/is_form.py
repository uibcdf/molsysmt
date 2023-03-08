def is_form(item):

    output = False

    if type(item)==str:
        if item.endswith('.h5') or item.endswith('.hdf5'):
            output = True

    return output

