
def query_dataframe(item, selection='all'):

    selection = selection.replace(".","_")
    item.columns = [column.replace(".", "_") for column in item.columns] 
    atom_indices = item.query(selection).index.to_numpy()
    return atom_indices

def parse(selection='all'):

    # "all", "backbone", "sidechain"

    parsed_selection = selection

    return parsed_selection

def dataframe_select(item, selection='all'):

    import inspect
    print("hola")
    print(inspect.stack()[1][0])
    print(inspect.stack()[1][0].f_globals['lista'])

    parsed_selection = parse(selection)
    atom_indices = query_dataframe(item, selection=parsed_selection)
    return atom_indices

