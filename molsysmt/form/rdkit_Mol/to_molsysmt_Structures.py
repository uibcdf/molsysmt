from molsysmt._private.argdigest import arg_digest
import numpy as np

@arg_digest(form='rdkit.Mol')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import Structures
    from molsysmt import pyunitwizard as puw
    from molsysmt._private.variables import is_all

    tmp_item = Structures()

    conformers = list(item.GetConformers())
    n_conformers = len(conformers)
    
    if n_conformers > 0:
        if is_all(structure_indices):
            structure_indices = range(n_conformers)
        
        coords = []
        structure_id = []
        for conformer_index in structure_indices:
            conf = conformers[conformer_index]
            coords.append(conf.GetPositions())
            structure_id.append(conf.GetId())
        
        # RDKit uses Angstroms
        output = np.array(coords)
        output = puw.quantity(output, 'angstroms')
        output = puw.standardize(output)
        
        if not is_all(atom_indices):
            output = output[:, atom_indices, :]

        tmp_item.append(
            structure_id=np.asarray(structure_id, dtype=np.int64),
            coordinates=output,
            skip_digestion=True,
        )

    return tmp_item
