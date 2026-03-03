from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='MDAnalysis.AtomGroup')
def to_MDAnalysis_Universe(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt._private.variables import is_all

    if is_all(atom_indices) and is_all(structure_indices):
        return item.universe.copy().atoms[item.indices].universe
    else:
        # Complex filtering via conversion to MolSys and back
        from molsysmt.basic import convert
        tmp_item = convert(item, to_form='molsysmt.MolSys', atom_indices=atom_indices, 
                           structure_indices=structure_indices, skip_digestion=True)
        return convert(tmp_item, to_form='MDAnalysis.Universe', skip_digestion=True)
