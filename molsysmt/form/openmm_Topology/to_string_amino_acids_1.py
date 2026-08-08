from molsysmt._private.argdigest import arg_digest
import numpy as np

@arg_digest(form='openmm.Topology')
def to_string_amino_acids_1(item, atom_indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology.to_string_amino_acids_1 import to_string_amino_acids_1 as molsysmt_Topology_to_string_amino_acids_1
    from . import get_group_index_from_atom

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    tmp_item = molsysmt_Topology_to_string_amino_acids_1(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

