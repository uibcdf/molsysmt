from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='pdbfixer.PDBFixer')
@dep_digest('pdbfixer')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of atoms or structures from form pdbfixer.PDBFixer.

    Parameters
    ----------
    item : pdbfixer.PDBFixer
        Source item.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices to extract.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    pdbfixer.PDBFixer
        Extracted subset in the same form.
    """

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:
            from copy import deepcopy
            tmp_item = deepcopy(item)
        else:
            tmp_item = item
    else:

        from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology
        from . import get_coordinates_from_atom
        from molsysmt.form.openmm_Topology.to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer as openmm_Topology_to_pdbfixer_PDBFixer

        coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                                skip_digestion=True)
        tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                      skip_digestion=True)
        tmp_item = openmm_Topology_to_pdbfixer_PDBFixer(tmp_item, coordinates=coordinates, skip_digestion=True)

    return tmp_item
