def is_file_msmpk(item):

    output = False

    if type(item)==str:
        output = item.endswith('.msmpk')

    return output

