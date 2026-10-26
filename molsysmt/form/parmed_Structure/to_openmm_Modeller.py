import numpy as np
from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="parmed.Structure")
@dep_digest("openmm")
def to_openmm_Modeller(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting from parmed.Structure to openmm.Modeller.


    Parameters
    ----------
    item : molecular system
        ParmEd structure supplying topology, coordinates and optional unit cells.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include. Selected atoms retain source order;
        repeated indices are included once.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include. Modeller represents the first
        selected structure and its cell; the default uses structure zero.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Modeller
        Selected topology and one set of positions, expressed in OpenMM units.
        The input structure is not modified.

    Examples
    --------
    >>> import molsysmt as msm
    >>> source = msm.convert(msm.systems['caffeine']['caffeine.mol2'],
    ...                      to_form='parmed.Structure')
    >>> converted = to_openmm_Modeller(source)
    >>> len(converted.positions) == len(source.atoms)
    True

    .. versionadded:: 1.0.0
    """

    from molsysmt._private.variables import is_all
    from molsysmt.form.openmm_Topology.set import set_box_to_system
    from molsysmt.form.openmm_Topology.to_openmm_Modeller import (
        to_openmm_Modeller as openmm_Topology_to_openmm_Modeller,
    )

    from . import get_box_from_system, get_coordinates_from_atom
    from .to_openmm_Topology import to_openmm_Topology

    if not is_all(atom_indices):
        atom_indices = np.unique(np.asarray(atom_indices, dtype=np.int64))

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    coordinates = get_coordinates_from_atom(
        item,
        indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    box = get_box_from_system(
        item, structure_indices=structure_indices, skip_digestion=True
    )
    if box is not None:
        set_box_to_system(tmp_item, value=box[:1], skip_digestion=True)
    tmp_item = openmm_Topology_to_openmm_Modeller(
        tmp_item, coordinates=coordinates, box=box, skip_digestion=True
    )

    return tmp_item
