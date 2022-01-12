def is_file(item):

    from molsysmt.forms import file_extensions_recognized

    output = False

    if type(item) is str:
        file_extension = item.split('.')[-1].lower()
        if file_extension in file_extensions_recognized:
            output = 'file:'+file_extension

    return output

