def item_is_file(item):

    from molsysmt.api_forms import file_apis
    from importlib import import_module

    output = False

    for file_api in file_apis:
        api = import_module(api, 'molsysmt.api_forms')
        if api.is_form(item):
            output = True
            break

    return output

