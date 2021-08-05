from molsysmt.tools.molecular_systems import *
from molsysmt.tools.items import compatibles_for_a_single_molecular_system as items_compatibles_for_a_single_molecular_system
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple
from molsysmt._private_tools.exceptions import *
from molsysmt.forms import dict_extract_item

molecular_system_components = {

    'elements' : False, # atoms, groups, chains, entities, etc.
    'bonds' : False, # bonds
    'coordinates' : False, # coordinates, steps, time
    'velocities' : False, # velocities
    'box' : False, # box or unit cell
    'ff_parameters' : False, # interatomic interaction parameters or force field
    'mm_parameters' : False, # molecular mechanics parameters to work with the interatomic interactions
    'thermo_state' : False, # thermodinamic state or parameters of the ensemble: T and P.
    'simulation' : False # Other simulation parameters to simulate the behaviour such as integrator, damping, etc.

}

class MolecularSystem():

    def __init__(self, items=None):

        self.elements_item, self.elements_form = None, None
        self.bonds_item, self.bonds_form = None, None
        self.coordinates_item, self.coordinates_form = None, None
        self.velocities_item, self.velocities_form = None, None
        self.box_item, self.box_form = None, None
        self.ff_parameters_item, self.ff_parameters_form = None, None
        self.mm_parameters_item, self.mm_parameters_form = None, None
        self.thermo_state_item, self.thermo_state_form = None, None
        self.simulation_item, self.simulation_form = None, None


        if items is not None:

            if type(items)==MolecularSystem:

                self.elements_item, self.elements_form = items.elements_item, items.elements_form
                self.bonds_item, self.bonds_form = items.bonds_item, items.bonds_form
                self.coordinates_item, self.coordinates_form = items.coordinates_item, items.coordinates_form
                self.velocities_item, self.velocities_form = items.velocities_item, items.velocities_form
                self.box_item, self.box_form = items.box_item, items.box_form
                self.ff_parameters_item, self.ff_parameters_form = items.ff_parameters_item, items.ff_parameters_form
                self.mm_parameters_item, self.mm_parameters_form = items.mm_parameters_item, items.mm_parameters_form
                self.thermo_state_item, self.thermo_state_form = items.thermo_state_item, items.thermo_state_form
                self.simulation_item, self.simulation_form = items.simulation_item, items.simulation_form

            else:

                if not is_list_or_tuple(items):
                    items = [items]

                aux_items = []
                for item in items:
                    if item is not None:
                        aux_items.append(item)
                items = aux_items

                if not is_a_single_molecular_system(items):
                    raise NeedsSingleMolecularSystemError()

                self.elements_item, self.elements_form = where_elements_in_molecular_system(items)
                self.bonds_item, self.bonds_form = where_bonds_in_molecular_system(items)
                self.coordinates_item, self.coordinates_form = where_coordinates_in_molecular_system(items)
                self.velocities_item, self.velocities_form = where_velocities_in_molecular_system(items)
                self.box_item, self.box_form = where_box_in_molecular_system(items)
                self.ff_parameters_item, self.ff_parameters_form = where_ff_parameters_in_molecular_system(items)
                self.mm_parameters_item, self.mm_parameters_form = where_mm_parameters_in_molecular_system(items)
                self.thermo_state_item, self.thermo_state_form = where_thermo_state_in_molecular_system(items)
                self.simulation_item, self.simulation_form = where_simulation_in_molecular_system(items)

    def get_items(self):

        items = []
        forms = []

        for component_name in molecular_system_components.keys():
            if getattr(self, component_name+'_item') is not None:
                if getattr(self, component_name+'_item') not in items:
                    items.append(getattr(self, component_name+'_item'))
                    forms.append(getattr(self, component_name+'_form'))

        return items, forms

    def extract(self, atom_indices='all', frame_indices='all'):

        tmp_molecular_system = MolecularSystem()
        extracted_items = {}

        for component_name in molecular_system_components.keys():

            aux_item = getattr(self, component_name+'_item')
            aux_form = getattr(self, component_name+'_form')

            if aux_item is not None:
                if aux_item not in extracted_items:
                    aux_extracted_item = dict_extract_item[aux_form](aux_item, atom_indices=atom_indices, frame_indices=frame_indices)
                    extracted_items[aux_item] = aux_extracted_item
                else:
                    aux_extracted_item = extracted_items[aux_item]
                setattr(tmp_molecular_system, component_name+'_item', aux_extracted_item)
                setattr(tmp_molecular_system, component_name+'_form', aux_form)

        del(extracted_items)

        return tmp_molecular_system

    def combine_with_items(self, items, atom_indices='all', frame_indices='all'):

        if not is_list_or_tuple(items):
            items = [items]

        items = list(filter(None.__ne__, items))

        output_molecular_system = MolecularSystem(items)

        extracted_items = {}

        for component_name in molecular_system_components.keys():

            if getattr(output_molecular_system, component_name+'_item' ) is None:
                if getattr(self, component_name+'_item' ) is not None:

                    aux_item = getattr(self, component_name+'_item')
                    aux_form = getattr(self, component_name+'_form')

                    if (atom_indices is not 'all') or (frame_indices is not 'all'):
                        if aux_item not in extracted_items:
                            aux_extracted_item = dict_extract_item[aux_form](aux_item, atom_indices=atom_indices, frame_indices=frame_indices)
                            extracted_items[aux_item] = aux_extracted_item
                        else:
                            aux_extracted_item = extracted_items[aux_item]
                        aux_item = aux_extracted_item

                    if items_compatibles_for_a_single_molecular_system(items+[aux_item]):

                        setattr(output_molecular_system, component_name+'_item', aux_item)
                        setattr(output_molecular_system, component_name+'_form', aux_form)

                    else:

                        raise ValueError("Combination of incompatible items in molecular system")

        del(extracted_items)

        return output_molecular_system

