from molsysmt._private.argdigest import arg_digest
import numpy as np

@arg_digest(form='mmcif.PdbxContainers.DataContainer')
def to_string_amino_acids_1(item, group_indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import to_string_amino_acids_1 as molsysmt_Topology_to_string_amino_acids_1

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    tmp_item = molsysmt_Topology_to_string_amino_acids_1(tmp_item, group_indices=group_indices, skip_digestion=True)

    return tmp_item

