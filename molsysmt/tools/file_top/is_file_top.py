def is_file_top(item):

    output = False

    if type(item)==str:
        output = item.endswith('.top')

    return output

