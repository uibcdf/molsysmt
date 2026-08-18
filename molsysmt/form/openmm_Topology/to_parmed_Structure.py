from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Topology')
def to_parmed_Structure(item, atom_indices='all', skip_digestion=False):
    """
    Converting from openmm.Topology to parmed.Structure.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    parmed.Structure
        Resulting object in parmed.Structure form.


    .. versionadded:: 1.0.0
    """

    from parmed.openmm import load_topology as openmm_Topology_to_parmed_Structure
    from .extract import extract

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)
    tmp_item = openmm_Topology_to_parmed_Structure(tmp_item)
    return tmp_item

