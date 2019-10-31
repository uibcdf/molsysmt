from .entity import Entity as _Entity

class SmallMolecule(_Entity):

    def __init__(self):

        super(_Entity,self).__init__()

        self.chemical_id = chemical_id
        self.inchikey = inchikey
        self.chembl_id = chembl_id

