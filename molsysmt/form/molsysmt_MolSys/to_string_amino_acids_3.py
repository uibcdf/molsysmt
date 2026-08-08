from molsysmt._private.argdigest import arg_digest
import numpy as np

@arg_digest(form='molsysmt.MolSys')
def to_string_amino_acids_3(item, group_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Topology.to_string_amino_acids_3 import to_string_amino_acids_3 as molsysmt_Topology_to_string_amino_acids_3

    tmp_item = molsysmt_Topology_to_string_amino_acids_3(item.topology, group_indices=group_indices, skip_digestion=True)

    return tmp_item

