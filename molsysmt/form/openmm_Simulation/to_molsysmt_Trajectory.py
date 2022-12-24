from molsysmt._private.digestion import digest

@digest(form='openmm.Simulation')
def to_molsysmt_Structures(item, selection='all', structure_indices='all', syntax='MolSysMT', digest=True):

    from molsysmt.basic import convert

    tmp_item = convert(item, to_form='molsysmt.Trajectory', selection=selection, structure_indices=structure_indices,
                       syntax=syntax, digest=False)

    return tmp_item

