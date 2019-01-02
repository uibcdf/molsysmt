## Igual seria una mejor estrategia hacer un data frame y que todo lo demas fuera como punteros al data frame


from MolecularUnit import _Unit, _unit_attribute_magnitude, _ListUnits  #Cambiar nombre de libreria (Tienen que ir con mayuscula los nombres de archivo?)
from MolecularDB import _AtomDB

####################################
# GENERAL COMMENTS


#
# END GENERAL COMMENTS
####################################

#Deberia de poner aqui una lista de inicializadores de clases para que todo fuera mas rapido. 
_atom_attribute_magnitude=[
    {'name':'mass',           'value':0.0,   'unit':None, 'dtype':None},
    {'name':'charge',         'value':0.0,   'unit':None, 'dtype':None},
    {'name':'vdw',            'value':0.0,   'unit':None, 'dtype':None},
    {'name':'bfactor',        'value':0.0,   'unit':None, 'dtype':None},
    {'name':'acceptor',       'value':False, 'unit':None, 'dtype':None},
    {'name':'donor',          'value':False, 'unit':None, 'dtype':None},
    {'name':'polarizability', 'value':False, 'unit':None, 'dtype':None},
    {'name':'coordinates',    'value':None,  'unit':None, 'dtype':None}
]

_atom_attribute_list=[
    {'name':'covalent_bonds', 'utype':'Atom'},
    {'name':'hbonds',         'utype':'Atom'}
]


class Atom(_Unit):

    _utype = 'Atom'

    def __init__(self):
     
        ###### Atributos universales sin discusion para todo atomo
        
        _Unit.__init__(self,subunit=None)
        # El atomo lo definimos como una unidad que no tiene subdivision
        # Atributos heredados de _Unit
        # self.name             = None
        # self.index            = None
        # self.type             = None                  # Atom nature (H,O,...)

        ###### Atributos adicionales especificos y universales para todo atomo
        
        for attribute in _atom_attribute_list:
            self._add_attribute_list(**attribute)

        for attribute in _atom_attribute_magnitude:
            self._add_attribute_magnitude(**attribute)
     
    def _add_attribute_magnitude(self,name=None,value=None,unit=None,dtype=None):
        setattr(self, name, _AtomAttribute(value,unit,dtype))

    def _add_attribute_list(self,name=None,utype=None):
        setattr(self, name, _ListUnits(utype=utype))

class _AtomAttribute():

    _utype = 'AtomAttribute'
    # Esto deberia ser otro abc collection... que se retorne el valor como en simtk, por ahora se queda asi
    def __init__(self,value=None,unit=None,dtype=None):
        self.value             = value
        self.unit              = unit
        self.dtype             = dtype

class Universe():
 
    def __init__(self):
 
        self.atom              = _ListUnits(utype=Atom)
        self._atomDB           = _AtomDB(attributes=_unit_attribute_magnitude+_atom_attribute_magnitude,number_atoms=None)

    def add_atom(self,atom=None):

        if not atom:
            atom=Atom()

        self.atom.append(atom)
        self._atomDB.add_atom(atom)

    def add_atom_attribute(self,name=None,value=None,unit=None,dtype=None):

        for atom in self.atom:
            atom.add_attribute(name=None,value=None,unit=None,dtype=None)


        # Posible estructura para probar, cada new group se convertira automaticamente en un nuevo atributo de los atomos

    #    self.new_group(name='molecule',unit='atom')
    #    self.molecule.new_group(name='residue',unit='atom')
    #    self.molecule.new_group(name='chain',unit='atom')
    #    self.new_group(name='water',unit='molecule')
    #    self.new_group(name='ion',unit='molecule')
    #    self.new_group(name='protein',unit='molecule')
    #    self.new_group(name='lipid',unit='molecule')
    # 
    #def selection(self,name=None,selection=None,syntax=None,verbose=False):
    # 
    #    self.new_selection(name,selection,syntax,verbose) # The input and output have to be _list_units(), y la sintaxis se deberia de poder elegir (VMD, Pymol, etc...)
    # 
    #    pass
    # 
    #def dump():
    #    pass
    # 
    #def load():
    #    pass
    # 
    #def new_group(self,name=None,unit=None): # en realidad es :_Unit:
    #    setattr(self, name, _Group(unit))
    #    pass
    #def remove_group(): # en realidad es :_Unit:
    #    pass
    #def merge_groups(): # en realidad es :_Unit:
    #    pass
    # 
    #def new_selection(): # en realidad es :_Unit:
    #    pass
    #def remove_selection(): # en realidad es :_Unit:
    #    pass
    #def merge_selections(): # en realidad es :_Unit:
    #    pass


    

#class molecule(_unit):
# 
#    def __init__(self):
# 
#        ###### Atributos universales sin discusion para toda molecula
# 
#        # Heredados de _unit
#        #self.name             = None
#        #self.index            = None
#        #self.__int_name       = None                  # internal name of unit
#        #self.__int_index      = None                  # internal index of unit
#        #self.type             = None                  # for molecules: protein,ion,lipid,water,... for atom: atom nature (H,O,...)
# 
#        self.atom              = _list_units()         # Todas las moleculas tienen una lista de atomos
# 
#        ###### Organizaciones supra-atomicas que puede tener una molecula pero que no tienen toooodas las moleculas
#        # Pensar como hacer esto.. para que no aparezcan si no estan
# 
#        self.set('residue')
#        self.set('chain')
# 
#    def new_group(self,name):
#        ''' creates new supramolecular set'''
#        return tools.set_list_units(self.atom,name)
#        pass
# 
#    def remove_group(self):
#        ''' removes supramolecular set'''
#        pass
# 
#    def merge_groups(self):
#        ''' removes supramolecular set'''
#        pass
# 
#    def select(self):
#        ''' selection '''
# 
#        selection=tools.selector(self.atom, syntax=None)    # The input and output have to be _list_units(), y la sintaxis se deberia de poder elegir (VMD, Pymol, etc...) 
# 
#        return selection
# 
#    def extract(self):
#        ''' creates a new and unlinked system '''
# 
#        pass
        
