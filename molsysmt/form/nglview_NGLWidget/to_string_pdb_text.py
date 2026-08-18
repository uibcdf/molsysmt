from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='nglview.NGLWidget')
def to_string_pdb_text(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from nglview.NGLWidget to string:pdb_text.

    Parameters
    ----------
    item : nglview.NGLWidget
        Source item in nglview.NGLWidget form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:pdb_text
        Resulting object in string:pdb_text form.

    .. versionadded:: 1.0.0
    """

    from ..string_pdb_text.extract import extract

    try:
        tmp_item = item.component_0.get_structure_string()
    except Exception:
        tmp_item = item.get_state()['_ngl_msg_archive'][0]['args'][0]['data']

    if not (is_all(atom_indices)*is_all(structure_indices)):

        tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    return tmp_item


