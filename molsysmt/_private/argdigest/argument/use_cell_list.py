from molsysmt._private.smonitor import ArgumentError


def digest_use_cell_list(use_cell_list, caller=None):

    if isinstance(use_cell_list, bool):
        return use_cell_list

    if isinstance(use_cell_list, str) and use_cell_list.lower() == 'auto':
        return 'auto'

    raise ArgumentError('use_cell_list', value=use_cell_list, caller=caller, message=None)
