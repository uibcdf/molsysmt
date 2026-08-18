from molsysmt._private.argdigest import arg_digest
import numpy as np

@arg_digest(form='openmm.Topology')
def to_string_amino_acids_1(item, atom_indices='all', skip_digestion=False):
    """
    Converting from openmm.Topology to string:amino_acids_1.

    Parameters
    ----------
    item : openmm.Topology
        Source item in openmm.Topology form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
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
    from . import get_group_index_from_atom

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    tmp_item = molsysmt_Topology_to_string_amino_acids_1(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

