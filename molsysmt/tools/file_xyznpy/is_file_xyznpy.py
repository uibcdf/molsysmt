def is_file_xyznpy(item):

    output = False

    if type(item)==str:
        output = item.endswith('.xyznpy')

    return output

