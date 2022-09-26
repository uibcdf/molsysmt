from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw

###### Set

## Atom

@digest(form='molsysmt.Topology')
def set_atom_name_to_atom(item, indices='all', structure_indices='all', value=None):

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


