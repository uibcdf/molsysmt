from molsysmt._private.arg_digestion import arg_digest
import numpy as np

@arg_digest(form='openff.Molecule')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt import pyunitwizard as puw
    from molsysmt.native import Structures
    from molsysmt._private.variables import is_all

    tmp_item = Structures()
    conformers = item.conformers
    if conformers is None:
        return tmp_item

    if is_all(structure_indices):
        structure_indices = range(len(conformers))
    selected = [conformers[index] for index in structure_indices]
    coordinates = np.asarray(
        [conformer.m_as('angstrom') for conformer in selected], dtype=np.float64
    )
    if not is_all(atom_indices):
        coordinates = coordinates[:, atom_indices, :]
    coordinates = puw.standardize(puw.quantity(coordinates, 'angstrom'))
    tmp_item.append(
        structure_id=np.asarray(list(structure_indices), dtype=np.int64),
        coordinates=coordinates,
        skip_digestion=True,
    )
    return tmp_item
