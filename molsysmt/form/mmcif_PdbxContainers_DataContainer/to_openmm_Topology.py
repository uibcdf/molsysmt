from .get_structural_attributes import *
from .get_topological_attributes import *

from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mmcif.PdbxContainers.DataContainer')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from mmcif.PdbxContainers.DataContainer to openmm.Topology.

    Parameters
    ----------
    item : mmcif.PdbxContainers.DataContainer
        Source item in mmcif.PdbxContainers.DataContainer form.
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
    from molsysmt.form.molsysmt_Topology.to_openmm_Topology import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology

    box = get_box_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = molsysmt_Topology_to_openmm_Topology(tmp_item, box=box, skip_digestion=True)

    return tmp_item

