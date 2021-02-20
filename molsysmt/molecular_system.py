from molsysmt.tools.molecular_systems import *

class MolecularSystem():

    def __init__(self, items):

        if not is_a_single_molecular_system(items):
            raise NeedsSingleMolecularSystem()

        self.topology_item, self.topology_form = where_topology_in_molecular_system(items)
        self.bonds_item, self.bonds_form = where_bonds_in_molecular_system(items)
        self.parameters_item, self.parameters_form = where_parameters_in_molecular_system(items)
        self.trajectory_item, self.trajectory_form = where_trajectory_in_molecular_system(items)
        self.coordinates_item, self.coordinates_form = where_coordinates_in_molecular_system(items)
        self.box_item, self.box_form = where_box_in_molecular_system(items)

