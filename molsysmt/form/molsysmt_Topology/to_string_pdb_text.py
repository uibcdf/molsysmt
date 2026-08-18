from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.Topology')
def to_string_pdb_text(item, atom_indices='all', coordinates=None, box=None, skip_digestion=False):
    """
    Converting from molsysmt.Topology to string:pdb_text.

    Parameters
    ----------
    item : molsysmt.Topology
        Source item in molsysmt.Topology form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : numpy.ndarray or quantity
        Cartesian coordinate array in nanometers.
    box : numpy.ndarray or quantity
        Simulation box vectors in nanometers.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:pdb_text
        Resulting object in string:pdb_text form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.native import MolSys, Structures
    from . import extract
    from molsysmt.form.molsysmt_MolSys.to_string_pdb_text import to_string_pdb_text as molsysmt_MolSys_to_string_pdb_text

    tmp_item =  MolSys()
    tmp_item.topology = extract(item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)
    tmp_item.structures.append(coordinates=coordinates, box=box, skip_digestion=True)
    tmp_item = molsysmt_MolSys_to_string_pdb_text(tmp_item, skip_digestion=True)

    return tmp_item


