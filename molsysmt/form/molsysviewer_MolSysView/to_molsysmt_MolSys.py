from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all


@digest(form='molsysviewer.MolSysView')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', get_missing_bonds=True,
                       skip_digestion=False):

    from molsysmt.basic import extract

    molsys = getattr(item, '_molsys', None)
    if molsys is None:
        return None

    if not (is_all(atom_indices) and is_all(structure_indices)):
        molsys = extract(molsys, selection=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    return molsys
