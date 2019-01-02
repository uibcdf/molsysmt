from collections import MutableSequence as colMutableSequence

_unit_attribute_magnitude=[
    {'name':'name',           'value':None,   'unit':None, 'dtype':None},
    {'name':'index',          'value':None,   'unit':None, 'dtype':None},
    {'name':'type',           'value':None,   'unit':None, 'dtype':None}
]


class _Unit():                             # Common attributes for unit objects (atoms and molecules)
    
    def __init__(self,subunit=None):
        self.name             = None
        self.index            = None
        self.type             = None                  # for residues: protein,ion,solv. for atom: atom_nature (H,O,...)
        self._utype           = None
        if subunit:
            setattr(self, subunit, _list_units)

#class _Group(colMutableSequence):
# 
#    def __init__(self,unit=None):
#        super(_ListUnits, self).__init__()
#        self._group = []
#        self._unit_type = unit
#        self.len    = self.__len__
# 
#    def __len__(self):
#        return len(self._group)
# 
#    def __getitem__(self, ii):
#        return self._group[ii]
# 
#    def __delitem__(self, ii):
#        del self._group[ii]
# 
#    def __setitem__(self, ii, val): # val is a :class: unit
#        self._group[ii] = val
#        return self._group[ii]
# 
#    def __str__(self):
#        return """<Group of %s>""" % self._unit_type
# 
#    def __repr__(self):
#        return """<Group of %s>""" % self._unit_type
# 
#    def insert(self, val):
#        self._group.insert(val)
# 
#    def append(self, val):
#        self._group.append(val)
# 
#    def extend(self, arg):
#        self._group.extend(arg)
# 
#    def add_group():
#        self.append(_Unit)



class _ListUnits(colMutableSequence):     # Common structure for list of units

    """Define a list format, which I can customize with colMutableSequence"""
    def __init__(self,arg=None,utype=None):       # arg can be a list of :class: unit
        super(_ListUnits, self).__init__()
        self._units = []                         #
        self.list   = []                         # lista publica de indices
        self.len    = self.__len__               # Numero de unidades
        self._utype  = _read_utype(utype)
        if arg :
            self._units = arg
            self.list   = [ii.index for ii in arg]

    def __len__(self):
        return len(self.list)

    def __getitem__(self, ii):
        return self._units[ii]

    def __delitem__(self, ii):
        del self._units[ii]
        del self.list[ii]

    def __setitem__(self, ii, val): # val is a :class: unit
        self._units[ii] = val
        self.list[ii] = val.index
        return self._list[ii]

    def __str__(self):
        return """<UList of %s %s>""" % (self._utype+'s', self.list)   # Tengo que poner esto mejor. definir plural.. o algo asi... o definir utype como clase..

    def __repr__(self):
        return """<UList of %s %s>""" % (self._utype+'s', self.list)

    def insert(self, val):
        self.list.insert(val.index)
        self._units.insert(val)

    def append(self, val):
        self.list.append(val.index)
        self._units.append(val)

    def extend(self, arg):
        self.list.extend(arg.list)
        self._units.extend(arg._units)


def _read_utype(utype=None):
    if utype in ['Atom','Molecule']:
        return utype
    else:
        try:
            utype._utype
        except:
            print 'error'
