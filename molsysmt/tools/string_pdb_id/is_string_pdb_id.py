def is_string_pdb_id(item):

    if type(item)!=str:
        raise ValueError

    output = False

    if item.startswith('pdb_id:'):

        output = True

    else:

        from sabueso.tools.string_pdb_id import is_string_pdb_id as sabueso_is_string_pdb_id

        output = sabueso_is_string_pdb_id(item)

    return output

