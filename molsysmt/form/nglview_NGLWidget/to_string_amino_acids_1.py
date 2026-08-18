from molsysmt._private.argdigest import arg_digest
import numpy as np

@arg_digest(form='nglview.NGLWidget')
def to_string_amino_acids_1(item, group_indices='all', skip_digestion=False):
    """
    Converting from nglview.NGLWidget to string:amino_acids_1.


    Parameters
    ----------
    item : molecular system
        Argument item.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Argument group_indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:amino_acids_1
        Resulting object in string:amino_acids_1 form.


    .. versionadded:: 1.0.0
    """

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology.to_string_amino_acids_1 import to_string_amino_acids_1 as molsysmt_Topology_to_string_amino_acids_1
    from . import get_atom_index_from_group

    atom_indices = get_atom_index_from_group(item, indices=group_indices, skip_digestion=True)
    atom_indices = np.concatenate(atom_indices, skip_digestion=True)
    tmp_item = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = molsysmt_Topology_to_string_amino_acids_1(tmp_item, skip_digestion=True)

    return tmp_item

