def is_file_h5(item):

    output = False

    if type(item)==str:
        if item.endswith('.h5') or item.endswith('.hdf5'):
            output = True

    return output

