
class Chain:

    """Chain element.

    Blablabla descripcion.

    Attributes
    ----------

    index : int
        Description of index.
    id : int or str
        Description of id.
    name : str
        Description of name.
    type : int
        Description of type.

    atom : list of objects
        Description of atom
    atom_indices : list of ints
        Description of atom
    n_atoms : list of ints
        Description of n_atoms

    group : list of objects
        Description of group
    group_indices : list of ints
        Description of group_indices
    n_groups : list of ints
        Description of n_groups

    component : list of objects
        Description of component
    component_indices : list of ints
        Description of component_indices
    n_components : list of ints
        Description of n_components

    entity : object
        Description of entity

    """

    def __init__(self, index=None, id=None, name=None, type=None,
                 atoms=[], groups=[], components=[]):

        self.index = index
        self.id = id
        self.name = name
        self.type = type

        self.atom = atoms
        self.atom_indices = [atom.index for atom in atoms]
        self.n_atoms = len(atoms)

        self.group = groups
        self.group_indices = [group.index for group in groups]
        self.n_groups = len(groups)

        self.component = components
        self.component_indices = [component.index for component in components]
        self.n_components = len(components)

        self.entity = None

    def formal_charge(self):

        value=0
        for atom in self.atom:
            value+=atom.formal_charge

        return value

    def add_atom (self, atom):

        self.atom.append(atom)
        self.atom_indices.append(atom.index)
        self.n_atoms+=1

    def add_group (self, group):

        self.group.append(group)
        self.group_indices.append(group.index)
        self.n_groups+=1

    def add_component (self, atom):

        self.component.append(component)
        self.component_indices.append(component.index)
        self.n_components+=1

    def copy(self):

        tmp_item = Chain(index=self.index, id=self.id, name=self.name)
        return tmp_item

    def _sanity_check (self, atoms=False, groups=False, components=False,
            entity=False, bioassembly=False, children_elements=False):

        from molsysmt.utils.exceptions import IncompleteElementError

        if atoms:
            if len(self.atom)==0:
                raise IncompleteElementError("Chain index {} has no atoms".format(self.index))
            elif children_elements:
                for atom in self.atom:
                    self.atom._sanity_check()

        if groups:
            if len(self.group)==0:
                raise IncompleteElementError("Chain index {} has no groups".format(self.index))
            elif children_elements:
                for group in self.group:
                    group._sanity_check()

        if components:
            if len(self.component)==0:
                raise IncompleteElementError("Chain index {} has no components".format(self.index))
            elif children_elements:
                for component in self.component:
                    component._sanity_check()

        if entity and (self.entity is None):
            raise IncompleteElementError("Chain index {} has no entity".format(self.index))

