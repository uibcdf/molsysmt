from molsysmt._private.argdigest import arg_digest
import numpy as np

@arg_digest(form='nglview.NGLWidget')
def to_string_amino_acids_3(item, group_indices='all', skip_digestion=False):
    """
    Converting from nglview.NGLWidget to string.amino.acids.3.

    Parameters
    ----------
    item : nglview.NGLWidget
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string.amino.acids.3
        Converted molecular system representation.
    """

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology.to_string_amino_acids_3 import to_string_amino_acids_3 as molsysmt_Topology_to_string_amino_acids_3
    from . import get_atom_index_from_group

    atom_indices = get_atom_index_from_group(item, indices=group_indices, skip_digestion=True)
    atom_indices = np.concatenate(atom_indices)
    tmp_item = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = molsysmt_Topology_to_string_amino_acids_3(tmp_item, skip_digestion=True)

    return tmp_item

