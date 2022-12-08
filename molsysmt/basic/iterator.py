from molsysmt._private.exceptions import NotImplementedIteratorError
#from molsysmt._private.exceptions import IteratorError

class Iterator():

    def __init__(self,
                 molecular_system,
                 element = 'system',
                 selection = 'all',
                 start = 0,
                 stop = None,
                 step = 1,
                 chunk = 1,
                 structure_indices = None,
                 syntax = "MolSysMT",
                 **kwargs
                 ):

        from . import select, get_form, where_is_attribute
        from molsysmt.api_forms import dict_structures_iterator, dict_topology_iterator

        self.molecular_system = molecular_system
        self.element = element
        self.atom_indices = select(molecular_system, selection=selection, syntax=syntax)
        self.start = start
        self.stop = stop
        self.step = step
        self.chunk = chunk
        self.structure_indices = structure_indices

        self.arguments = []
        for ii, key in enumerate(kwargs.keys()):
            if kwargs[key]:
                self.arguments.append(key)

        if len(self.arguments)==0:
            self.arguments = ['structure_id', 'time', 'coordinates', 'box']

        self.position = 0

        self._iterators = []
        self._output = {ii:None for ii in self.arguments}

        aux_items_forms = {}
        aux_items_arguments = {}

        for argument in self.arguments:
            item, form = where_is_attribute(self.molecular_system, argument)
            if item in aux_items_forms:
                aux_items_arguments[item].append(argument)
            else:
                aux_items_forms[item]=form
                aux_items_arguments[item]=[argument]

        for item in aux_items_forms:

           tmp_arguments = {ii:True for ii in aux_items_arguments[item]}
           tmp_iterator = dict_structures_iterator[aux_items_forms[item]](item, atom_indices=self.atom_indices, start=self.start,
                   stop=self.stop, step=self.step, chunk=self.chunk, structure_indices=structure_indices, **tmp_arguments)

           self._iterators.append(tmp_iterator)

        del(aux_items_forms, aux_items_arguments)

    def __iter__(self):
        
        return self

    def __next__(self):

        if self.position <= self.stop:

            output = []

            for iterator in iterators:

                output += iterator.__next__()

            return output

        else:

            raise StopIteration

