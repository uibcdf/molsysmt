from molsysmt._private.digestion import digest

@digest(form='string:pdb_id')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from . import to_bcifreader_PdbxContainers_DataContainer
    from ..bcifreader_PdbxContainers_DataContainer import to_molsysmt_Topology as bcifreader_PdbxContainers_DataContainer_to_molsysmt_Topology

    tmp_item = to_bcifreader_PdbxContainers_DataContainer(item, skip_digestion=True)
    tmp_item = bcifreader_PdbxContainers_DataContainer_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

