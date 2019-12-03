
def query_dataframe(item, selection='all'):

    if '@' in selection:
        from inspect import stack
        count = 0
        for stack_frame in stack():
            count +=1
            if stack_frame.function == 'select':
                break
        var_names = [name[1:] for name in selection.split(' ') if name.startswith('@')]
        for var_name in var_names:
            globals()[var_name]=stack()[count][0].f_globals[var_name]

    selection = selection.replace(".","_")
    item.columns = [column.replace(".", "_") for column in item.columns]
    atom_indices = item.query(selection).index.to_numpy()
    item.columns = [column.replace("_", ".") for column in item.columns]
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

