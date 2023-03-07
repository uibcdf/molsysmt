from molsysmt._private.digestion import digest

@digest(form='openmm.Simulation')
def to_molsysmt_Structures(item, selection='all', structure_indices='all', syntax='MolSysMT'):

    from molsysmt.basic import convert

    tmp_item = convert(item, to_form='molsysmt.Trajectory', selection=selection, structure_indices=structure_indices,
                       syntax=syntax)

    return tmp_item

def _to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    return to_molsysmt_Structures(item, structure_indices='all')
