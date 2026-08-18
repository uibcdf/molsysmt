from molsysmt._private.argdigest import arg_digest
import numpy as np

@arg_digest(form='biopython.PDBStructure')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from biopython.PDBStructure to molsysmt.Structures.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Structures
        Resulting object in molsysmt.Structures form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.native import Structures
    from molsysmt import pyunitwizard as puw
    from molsysmt._private.variables import is_all

    models = list(item.get_models())
    n_models = len(models)

    if is_all(structure_indices):
        structure_indices = range(n_models)

    tmp_item = Structures()

    coords = []
    for model_idx in structure_indices:
        model = models[model_idx]
        model_coords = []
        for atom in model.get_atoms():
            model_coords.append(atom.coord)
        coords.append(model_coords)

    output = np.array(coords)
    # BioPython uses Angstroms
    output = puw.quantity(output, 'angstroms')
    output = puw.standardize(output)

    if not is_all(atom_indices):
        output = output[:, atom_indices, :]

    tmp_item.append(coordinates=output, skip_digestion=True)

    return tmp_item
