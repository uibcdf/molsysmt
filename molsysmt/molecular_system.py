from molsysmt.tools.molecular_systems import *
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple

class MolecularSystem():

    def __init__(self, items):

        if not is_list_or_tuple(items):
            items = [items]

        if not is_a_single_molecular_system(items):
            raise NeedsSingleMolecularSystem()

        self.topology_item, self.topology_form = where_topology_in_molecular_system(items)
        self.bonds_item, self.bonds_form = where_bonds_in_molecular_system(items)
        self.parameters_item, self.parameters_form = where_parameters_in_molecular_system(items)
        self.coordinates_item, self.coordinates_form = where_coordinates_in_molecular_system(items)
        self.box_item, self.box_form = where_box_in_molecular_system(items)

    def get_items(self):

        items = []
        forms = []

        if self.topology_item is not None:
            items.append(self.topology_item)
            forms.append(self.topology_form)

        if self.bonds_item is not None:
            if self.bonds_item not in items:
                items.append(self.bonds_item)
                forms.append(self.bonds_form)

        if self.parameters_item is not None:
            if self.parameters_item not in items:
                items.append(self.parameters_item)
                forms.append(self.parameters_form)

        if self.coordinates_item is not None:
            if self.coordinates_item not in items:
                items.append(self.coordinates_item)
                forms.append(self.coordinates_form)

        if self.box_item is not None:
            if self.box_item not in items:
                items.append(self.box_item)
                forms.append(self.box_form)

        if len(items)==1:
            items = items[0]
            forms = forms[0]

        return items, forms


    def combine_with_items(self, items):

        if not is_list_or_tuple(items):
            items = [items]

        tmp_molecular_system = MolecularSystem(items)

        if tmp_molecular_system.topology_item is None and self.topology_item is not None:
            tmp_items = items+[self.topology_item]
            if is_a_single_molecular_system(tmp_items):
                tmp_molecular_system.topology_item = self.topology_item
                tmp_molecular_system.topology_form = self.topology_form

        if tmp_molecular_system.bonds_item is None and self.bonds_item is not None:
            tmp_items = items+[self.bonds_item]
            if is_a_single_molecular_system(tmp_items):
                tmp_molecular_system.bonds_item = self.bonds_item
                tmp_molecular_system.bonds_form = self.bonds_form

        if tmp_molecular_system.parameters_item is None and self.parameters_item is not None:
            tmp_items = items+[self.parameters_item]
            if is_a_single_molecular_system(tmp_items):
                tmp_molecular_system.parameters_item = self.parameters_item
                tmp_molecular_system.parameters_form = self.parameters_form

        if tmp_molecular_system.coordinates_item is None and self.coordinates_item is not None:
            tmp_items = items+[self.coordinates_item]
            if is_a_single_molecular_system(tmp_items):
                tmp_molecular_system.coordinates_item = self.coordinates_item
                tmp_molecular_system.coordinates_form = self.coordinates_form

        if tmp_molecular_system.box_item is None and self.box_item is not None:
            tmp_items = items+[self.box_item]
            if is_a_single_molecular_system(tmp_items):
                tmp_molecular_system.box_item = self.box_item
                tmp_molecular_system.box_form = self.box_form

        return tmp_molecular_system

