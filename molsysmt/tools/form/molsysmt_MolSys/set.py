from .is_molsysmt_MolSys import is_molsysmt_MolSys
from molsysmt._private_tools.exceptions import WrongFormError, WrongIndicesError, WrongStructureIndicesError
from molsysmt._private_tools.exceptions import NotImplementedMethodError
from molsysmt._private_tools.indices import digest_indices
from molsysmt._private_tools.structure_indices import digest_structure_indices
from molsysmt import puw

###### Set

## Atom

def set_atom_name_to_atom(item, indices='all', structure_indices='all', value=None, check=True):

    if check:

        try:
            is_molsysmt_MolSys(item)
        except:
            raise WrongFormError('molsysmt.MolSys')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt.tools.molsysmt_Topology import set_atom_name_to_atom as _set

    return _set(item.topology, indices=indices, structure_indices=structure_indices, value=value, check=True)

def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None, check=True):

    if check:

        try:
            is_molsysmt_MolSys(item)
        except:
            raise WrongFormError('molsysmt.MolSys')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    value = puw.standardize(value)

    if indices is 'all':
        if item.structures.coordinates.shape[1]!=value.shape[1]:
            raise ValueError('New coordinates array has different number of atoms')

    if structure_indices is 'all':
        if item.structures.coordinates.shape[0]!=value.shape[0]:
            raise ValueError('New coordinates array has different number of frames')

    if indices is 'all':
        if structure_indices is 'all':
            item.structures.coordinates[:,:,:] = value[:,:,:]
        else:
            item.structures.coordinates[structure_indices,:,:] = value[:,:,:]
    else:
        if structure_indices is 'all':
            item.structures.coordinates[:,indices,:] = value[:,:,:]
        else:
            item.structures.coordinates[np.ix_(structure_indices, indices)]=value[:,:,:]

## System

def set_box_to_system(item, indices='all', structure_indices='all', value=None, check=True):

    if check:

        try:
            is_molsysmt_MolSys(item)
        except:
            raise WrongFormError('molsysmt.MolSys')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    item.trajectory.box = value
    pass

def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None, check=True):

    if check:

        try:
            is_molsysmt_MolSys(item)
        except:
            raise WrongFormError('molsysmt.MolSys')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    return set_coordinates_to_atom(item, indices='all', structure_indices=structure_indices,
            value=value, check=False)

