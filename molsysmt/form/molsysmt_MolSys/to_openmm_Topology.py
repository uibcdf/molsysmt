from molsysmt._private.argdigest import arg_digest

from smonitor import signal

@signal(tags=['conversion'])
@arg_digest(form='molsysmt.MolSys')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to openmm.Topology.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Topology
        Resulting object in openmm.Topology form.

    .. versionadded:: 1.0.0
    """

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from . import get_box_from_system
    from molsysmt.form.molsysmt_Topology.to_openmm_Topology import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology

    tmp_item = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    box = get_box_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item = molsysmt_Topology_to_openmm_Topology(tmp_item, box=box, skip_digestion=True)

    return tmp_item

