from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='openmm.GromacsGroFile')
@dep_digest('openmm')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from openmm.GromacsGroFile to molsysmt.Topology.

    Parameters
    ----------
    item : openmm.GromacsGroFile
        Source item in openmm.GromacsGroFile form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.native import Topology
    from molsysmt.element.group import get_group_type_from_group_name
    from molsysmt.form.molsysmt_Topology.extract import extract as extract_molsysmt_Topology

    n_atoms = len(item.atomNames)

    # Build group mapping from consecutive (residueId, residueName) changes
    group_index_of_atoms = []
    group_ids = []
    group_names = []
    prev = None
    g_idx = -1
    for resid, resname in zip(item.residueIds, item.residueNames):
        curr = (resid, resname)
        if curr != prev:
            g_idx += 1
            group_ids.append(str(resid))
            group_names.append(resname)
            prev = curr
        group_index_of_atoms.append(g_idx)

    n_groups = g_idx + 1
    group_types = [get_group_type_from_group_name(name) for name in group_names]

    tmp_item = Topology(n_atoms=n_atoms, n_groups=n_groups)

    tmp_item.atoms['atom_name'] = list(item.atomNames)
    tmp_item.atoms['group_index'] = group_index_of_atoms

    tmp_item.groups['group_id'] = group_ids
    tmp_item.groups['group_name'] = group_names
    tmp_item.groups['group_type'] = group_types

    tmp_item.rebuild_components()
    tmp_item.rebuild_molecules()
    tmp_item.rebuild_entities()

    if not is_all(atom_indices):
        tmp_item = extract_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
