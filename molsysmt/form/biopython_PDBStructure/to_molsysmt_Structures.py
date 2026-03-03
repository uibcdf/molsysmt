from molsysmt._private.arg_digestion import arg_digest
import numpy as np

@arg_digest(form='biopython.PDBStructure')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

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
