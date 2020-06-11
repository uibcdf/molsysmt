
def query_dataframe(item, selection='all'):

    from re import findall
    from numpy import ndarray

    if '@' in selection:

        var_names = [ii[1:] for ii in findall(r"@[\w']+", selection)]
        first_var_name = var_names[0]

        from inspect import stack
        f_with_vars = None
        for stack_frame in stack():
            if first_var_name in stack_frame[0].f_globals.keys():
                f_with_vars = stack_frame[0].f_globals
                break
            elif first_var_name in stack_frame[0].f_locals.keys():
                f_with_vars = stack_frame[0].f_locals

        if f_with_vars is None:
            raise ValueError("An @variable in a selection sentence was not found")

        for var_name in var_names:
            var_value = f_with_vars[var_name]
            if type(var_value) in [ndarray]:
                var_value = list(var_value)
            locals()[var_name]=var_value

    atom_indices = item.query(selection).index.to_numpy()

    return atom_indices

def parse(selection='all'):

    # "all", "backbone", "sidechain"

    parsed_selection = selection

    return parsed_selection

def dataframe_select(item, selection='all', output_indices='atom'):

    parsed_selection = parse(selection)
    indices = query_dataframe(item, selection=parsed_selection)
    if output_indices in ['group', 'component', 'chain', 'molecule', 'entity']:
        from numpy import unique
        indices = item.iloc[indices][output_indices+'.index'].values
        indices = unique(indices)
    elif output_indices!='atom':
        raise ValueError('Wrong input argument in "ouput_indices"')
    return indices

