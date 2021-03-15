from molsysmt.tools.molecular_systems import *
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple

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

    def __init__(self, items):

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

            if not is_a_single_molecular_system(items):
                raise NeedsSingleMolecularSystem()


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

        if self.elements_item is not None:
            items.append(self.elements_item)
            forms.append(self.elements_form)

        if self.bonds_item is not None:
            if self.bonds_item not in items:
                items.append(self.bonds_item)
                forms.append(self.bonds_form)

        if self.coordinates_item is not None:
            if self.coordinates_item not in items:
                items.append(self.coordinates_item)
                forms.append(self.coordinates_form)

        if self.velocities_item is not None:
            if self.velocities_item not in items:
                items.append(self.velocities_item)
                forms.append(self.velocities_form)

        if self.box_item is not None:
            if self.box_item not in items:
                items.append(self.box_item)
                forms.append(self.box_form)

        if self.ff_parameters_item is not None:
            if self.ff_parameters_item not in items:
                items.append(self.ff_parameters_item)
                forms.append(self.ff_parameters_form)

        if self.mm_parameters_item is not None:
            if self.mm_parameters_item not in items:
                items.append(self.mm_parameters_item)
                forms.append(self.mm_parameters_form)

        if self.thermo_state_item is not None:
            if self.thermo_state_item not in items:
                items.append(self.thermo_state_item)
                forms.append(self.thermo_state_form)

        if self.simulation_item is not None:
            if self.simulation_item not in items:
                items.append(self.simulation_item)
                forms.append(self.simulation_form)

        return items, forms

    def combine_with_items(self, items):

        if not is_list_or_tuple(items):
            items = [items]

        tmp_molecular_system = MolecularSystem(items)

        if tmp_molecular_system.elements_item is None and self.elements_item is not None:
            tmp_items = items+[self.elements_item]
            if is_a_single_molecular_system(tmp_items):
                tmp_molecular_system.elements_item = self.elements_item
                tmp_molecular_system.elements_form = self.elements_form

        if tmp_molecular_system.bonds_item is None and self.bonds_item is not None:
            tmp_items = items+[self.bonds_item]
            if is_a_single_molecular_system(tmp_items):
                tmp_molecular_system.bonds_item = self.bonds_item
                tmp_molecular_system.bonds_form = self.bonds_form

        if tmp_molecular_system.coordinates_item is None and self.coordinates_item is not None:
            tmp_items = items+[self.coordinates_item]
            if is_a_single_molecular_system(tmp_items):
                tmp_molecular_system.coordinates_item = self.coordinates_item
                tmp_molecular_system.coordinates_form = self.coordinates_form

        if tmp_molecular_system.velocities_item is None and self.velocities_item is not None:
            tmp_items = items+[self.velocities_item]
            if is_a_single_molecular_system(tmp_items):
                tmp_molecular_system.velocities_item = self.velocities_item
                tmp_molecular_system.velocities_form = self.velocities_form

        if tmp_molecular_system.box_item is None and self.box_item is not None:
            tmp_items = items+[self.box_item]
            if is_a_single_molecular_system(tmp_items):
                tmp_molecular_system.box_item = self.box_item
                tmp_molecular_system.box_form = self.box_form

        if tmp_molecular_system.ff_parameters_item is None and self.ff_parameters_item is not None:
            tmp_items = items+[self.ff_parameters_item]
            if is_a_single_molecular_system(tmp_items):
                tmp_molecular_system.ff_parameters_item = self.ff_parameters_item
                tmp_molecular_system.ff_parameters_form = self.ff_parameters_form

        if tmp_molecular_system.mm_parameters_item is None and self.mm_parameters_item is not None:
            tmp_items = items+[self.mm_parameters_item]
            if is_a_single_molecular_system(tmp_items):
                tmp_molecular_system.mm_parameters_item = self.mm_parameters_item
                tmp_molecular_system.mm_parameters_form = self.mm_parameters_form

        if tmp_molecular_system.thermo_state_item is None and self.thermo_state_item is not None:
            tmp_items = items+[self.thermo_state_item]
            if is_a_single_molecular_system(tmp_items):
                tmp_molecular_system.thermo_state_item = self.thermo_state_item
                tmp_molecular_system.thermo_state_form = self.thermo_state_form

        if tmp_molecular_system.simulation_item is None and self.simulation_item is not None:
            tmp_items = items+[self.simulation_item]
            if is_a_single_molecular_system(tmp_items):
                tmp_molecular_system.simulation_item = self.simulation_item
                tmp_molecular_system.simulation_form = self.simulation_form

        return tmp_molecular_system

