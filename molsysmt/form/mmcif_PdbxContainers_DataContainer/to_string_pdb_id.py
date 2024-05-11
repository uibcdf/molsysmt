from molsysmt._private.digestion import digest

@digest(form='mmcif.PdbxContainers.DataContainer')
def to_string_pdb_text(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    raise NotImplementedError()

