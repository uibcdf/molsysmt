from molsysmt._private.digestion import digest

@digest
def to_string_aminoacids3(item, atom_indices='all', digest=True):

    from . import to_openmm_Topology

    tmp_item  = to_openm_Topology(item, atom_indices=atom_indices, digest=False)
    tmp_item = ''.join([ r.name for r in tmp_item.groups() ])

    return tmp_item

