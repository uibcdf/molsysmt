from molsysmt.tools.molecular_systems import *

class MolecularSystem():

    def __init__(self, items):

        if not is_a_single_molecular_system(items):
            raise NeedsSingleMolecularSystem()

        self.topology_item, self.topology_form = where_topology_in_molecular_system(items)
        self.bonds_item, self.bonds_form = where_bonds_in_molecular_system(items)
        self.parameters_item, self.parameters_form = where_parameters_in_molecular_system(items)
        self.coordinates_item, self.coordinates_form = where_coordinates_in_molecular_system(items)
        self.box_item, self.box_form = where_box_in_molecular_system(items)

def items_from_molecular_system(molecular_system):

    items = []
    forms = []

    if molecular_system.topology_item is not None:
        items.append(molecular_system.topology_item)
        forms.append(molecular_system.topology_form)

    if molecular_system.bonds_item is not None:
        if molecular_system.bonds_item not in items:
            items.append(molecular_system.bonds_item)
            forms.append(molecular_system.bonds_form)

    if molecular_system.parameters_item is not None:
        if molecular_system.parameters_item not in items:
            items.append(molecular_system.parameters_item)
            forms.append(molecular_system.parameters_form)

    if molecular_system.coordinates_item is not None:
        if molecular_system.coordinates_item not in items:
            items.append(molecular_system.coordinates_item)
            forms.append(molecular_system.coordinates_form)

    if molecular_system.box_item is not None:
        if molecular_system.box_item not in items:
            items.append(molecular_system.box_item)
            forms.append(molecular_system.box_form)

    if len(items)==1:
        items = items[0]
        forms = forms[0]

    return items, forms

