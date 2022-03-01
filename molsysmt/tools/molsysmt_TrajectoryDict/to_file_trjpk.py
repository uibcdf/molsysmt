
def to_file_trjpk(item, selection='all', structure_indices='all', output_filename=None, syntaxis='MolSysMT'):

    from molsysmt.tools.molsysmt_TrajectoryDict import is_molsymst_TrajectoryDict
    from molsysmt.basic import convert

    if not is_molsysmt_TrajectoryDict(item):
        raise ValueError

    if output_filename is None:
        raise ValueError

    tmp_item = convert(item, to_form=output_filename, selection=selection,
            structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

