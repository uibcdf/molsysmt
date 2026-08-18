from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='openmm.PDBFile')
@dep_digest('openmm')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of elements or structures from form openmm.PDBFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    copy_if_all : object, default=True
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.PDBFile
        Resulting object in openmm.PDBFile form.


    .. versionadded:: 1.0.0
    """

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:
            from copy import deepcopy
            tmp_item = deepcopy(item)
        else:
            tmp_item = item
    else:

        from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology
        from . import get_coordinates_from_atom, get_box_from_atom
        from molsysmt.form.openmm_Topology.to_openmm_PDBFile import to_openmm_PDBFile as openmm_Topology_to_openmm_PDBFile

        tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
        coordinates = get_coordinates_from_atom(tmp_item, atom_indices=atom_indices, skip_digestion=True)
        box = get_box_from_atom(tmp_item, skip_digestion=True)
        tmp_item = openmm_Topology_to_openmm_PDBFile(tmp_item, coordinates=coordinates, box=box, skip_digestion=True)

    return tmp_item

