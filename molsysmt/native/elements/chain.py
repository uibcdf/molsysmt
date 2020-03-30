
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

    bioassembly : object
        Description of bioassembly

    """

    def __init__(self, index=None, id=None, name=None, type=None):

        self.index = index
        self.id = id
        self.name = name
        self.type = type

        self.atom = []
        self.atom_indices = []
        self.n_atoms = 0

        self.group = []
        self.group_indices = []
        self.n_groups = 0

        self.component = []
        self.component_indices = []
        self.n_components = 0

        self.entity = None
        self.bioassembly = None

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

        if bioassembly and (self.bioassembly is None):
            raise IncompleteElementError("Chain index {} has no bioassembly".format(self.index))

    def _update_atoms(self):

        self.n_atoms = len(self.atom)
        self.atom_indices = [atom.index for atom in self.atom]

    def _update_groups(self, children_elements=False):

        self.n_groups = len(self.group)
        self.group_indices = [group.index for group in self.group]
        if children_elements:
            for group in self.group:
                group._update_all()

    def _update_components(self, children_elements=False):

        self.n_components = len(self.component)
        self.component_indices = [component.index for component in self.component]
        if children_elements:
            for component in self.component:
                component._update_all()

    def _update_all(self, children_elements=False):

        self._update_atoms()
        self._update_groups(children_elements=children_elements)
        self._update_components(children_elements=children_elements)

def chain_init_wizard(index=None, id=None, name=None, type=None):

    return Chain(index=index, id=id, name=name, type=type)

