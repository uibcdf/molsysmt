from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.Topology')
def to_string_pdb_text(item, atom_indices='all', coordinates=None, box=None, skip_digestion=False):
    """
    Converting from molsysmt.Topology to string.pdb.text.

    Parameters
    ----------
    item : molsysmt.Topology
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string.pdb.text
        Converted molecular system representation.
    """

    from molsysmt.native import MolSys, Structures
    from . import extract
    from molsysmt.form.molsysmt_MolSys.to_string_pdb_text import to_string_pdb_text as molsysmt_MolSys_to_string_pdb_text

    tmp_item =  MolSys()
    tmp_item.topology = extract(item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)
    tmp_item.structures.append(coordinates=coordinates, box=box, skip_digestion=True)
    tmp_item = molsysmt_MolSys_to_string_pdb_text(tmp_item, skip_digestion=True)

    return tmp_item


