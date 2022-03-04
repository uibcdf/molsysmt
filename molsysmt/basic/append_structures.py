from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.digestion import *
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple
from molsysmt.api_forms import dict_append_structures
from molsysmt.tools.molecular_system import are_multiple_molecular_systems
from molsysmt.tools.molecular_system import is_molecular_system


def append_structures(to_molecular_system, from_molecular_systems, selections='all',
        structure_indices='all', syntaxis='MolSysMT', check=True):


    if check:

        if not is_molecular_system(to_molecular_system):
            raise MolecularSystemNeededError()

        if not is_molecular_system(from_molecular_system):
            if not are_multiple_molecular_systems(from_molecular_system):
                raise MolecularSystemNeededError()

        raise NotImplementedError()

        try:
            syntaxis = digest_syntaxis(syntaxis)
        except:
            raise WrongSyntaxisError(syntaxis)

        try:
            selection = digest_selection(selection, syntaxis)
        except:
            raise WrongSelectionError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt.basic import convert, extract, get

    n_from_molecular_systems = len(from_molecular_systems)

    if not is_list_or_tuple(selections):
        selections = [selections for ii in range(n_from_molecular_systems)]
    elif len(selections)!=n_from_molecular_systems:
        raise ValueError("The length of the lists items and selections need to be equal.")

    if not is_list_or_tuple(structure_indices):
        structure_indices = [digest_structure_indices(structure_indices) for ii in range(n_from_molecular_systems)]
    elif len(structure_indices)!=n_from_molecular_systems:
        raise ValueError("The length of the lists items and structure_indices need to be equal.")

    box_in_diff_item=False
    if to_molecular_system.coordinates_item != to_molecular_system.box_item:
        box_in_diff_item=True

    for aux_molecular_system, aux_selection, aux_structure_indices in zip(from_molecular_systems, selections, structure_indices):

        step, time, coordinates, box = get(aux_molecular_system, target='atom',
                selection=aux_selection, structure_indices=aux_structure_indices, frame=True,
                check=False)

        if box_in_diff_item:
            dict_append_structures[to_molecular_system.coordinates_form](to_molecular_system.coordinates_item, step=step, time=time, coordinates=coordinates, box=None)
            dict_append_structures[to_molecular_system.box_form](to_molecular_system.box_item, step=None, time=None, coordinates=None, box=box)
        else:
            dict_append_structures[to_molecular_system.coordinates_form](to_molecular_system.coordinates_item, step=step, time=time, coordinates=coordinates, box=box)

    pass
