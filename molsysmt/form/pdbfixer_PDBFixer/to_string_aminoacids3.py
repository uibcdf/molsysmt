from molsysmt._private.digestion import digest

@digest(form='pdbfixer.PDBFixer')
def to_string_aminoacids3(item, atom_indices='all'):

    from . import to_openmm_Topology

    tmp_item  = to_openm_Topology(item, atom_indices=atom_indices)
    tmp_item = ''.join([ r.name for r in tmp_item.groups() ])

    return tmp_item

def _to_string_aminoacids3(item, atom_indices='all', structure_indices='all'):

    return to_string_aminoacids3(item, atom_indices=atom_indices, structure_indices=structure_indices)

