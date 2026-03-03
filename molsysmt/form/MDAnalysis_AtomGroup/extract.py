from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='MDAnalysis.AtomGroup')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    if is_all(atom_indices) and is_all(structure_indices):
        return item
    else:
        # MDAnalysis extract returns a new AtomGroup or Universe
        indices = item.indices
        if not is_all(atom_indices):
            indices = indices[atom_indices]
        
        if is_all(structure_indices):
            return item.universe.atoms[indices]
        else:
            # Multi-frame extraction requires creating a new universe or using slices
            from molsysmt.basic import extract as msm_extract
            return msm_extract(item.universe, selection=indices, structure_indices=structure_indices, 
                               to_form='MDAnalysis.AtomGroup', skip_digestion=True)
