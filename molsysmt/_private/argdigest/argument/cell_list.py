from molsysmt._private.smonitor import ArgumentError


def digest_cell_list(cell_list, caller=None):

    if cell_list is None:
        return None

    if isinstance(cell_list, bool):
        return cell_list

    if isinstance(cell_list, str):
        c_lower = cell_list.lower()
        if c_lower in ['auto']:
            return 'auto'
        if c_lower in ['true', 'yes', 'on']:
            return True
        if c_lower in ['false', 'no', 'off']:
            return False

    raise ArgumentError('cell_list', value=cell_list, caller=caller, message=None)
