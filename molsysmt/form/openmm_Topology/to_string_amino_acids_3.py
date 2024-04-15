from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_string_amino_acids_3(item, atom_indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import to_string_amino_acids_3 as molsysmt_Topology_to_string_amino_acids_3

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    tmp_item = molsysmt_Topology_to_string_amino_acids_3(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

