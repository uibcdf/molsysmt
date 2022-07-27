from molsysmt._private.digestion import digest_item as _digest_item
from molsysmt._private.digestion import digest_indices as _digest_indices
from molsysmt._private.digestion import digest_structure_indices as _digest_structure_indices
from molsysmt import puw as _puw

###### Set

## Atom

def set_atom_name_to_atom(item, indices='all', structure_indices='all', value=None):

    if check:

        _digest_item(item, 'molsysmt.Topology')
        indices = _digest_indices(indices)
        structure_indices = _digest_structure_indices(structure_indices)

    item.atoms_dataframe.loc[indices, 'atom_name']=value

    pass

##### System
#
#def set_box_to_system(item, structure_indices='all', value=None):
#
#    if check:
#
#        try:
#            is_molsysmt_Topology(item)
#        except:
#            raise WrongFormError('molsysmt.Topology')
#
#        try:
#            structure_indices = digest_structure_indices(structure_indices)
#        except:
#            raise WrongStructureIndicesError()
#
#        try:
#            box = digest_box(value)
#        except:
#            raise WrongStructureIndicesError()
#
#    box = puw.convert(box, to_unit='nm', to_form='openmm.unit')
#
#    print(np.shape(box))
#
#    pass


