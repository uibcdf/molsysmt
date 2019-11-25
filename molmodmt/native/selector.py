
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
    return atom_indices

def parse(selection='all'):

    # "all", "backbone", "sidechain"

    parsed_selection = selection

    return parsed_selection

def dataframe_select(item, selection='all'):

    parsed_selection = parse(selection)
    atom_indices = query_dataframe(item, selection=parsed_selection)
    return atom_indices
