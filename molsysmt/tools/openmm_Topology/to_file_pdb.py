
def to_file_pdb(item, selection='all', structure_indices='all', output_filename=None, syntaxis='MolSysMT'):

    from molsysmt.tools.openmm_Topology import is_openmm_Topology
    from molsysmt.basic import convert

    if not is_openmm_Topology(item):
        raise ValueError

    if output_filename is None:
        raise ValueError

    tmp_item = convert(item, to_form=output_filename, selection=selection,
            structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

