from molsysmt import select, get_form

#from molsysmt import get_form, convert
#from molsysmt.form.mdtraj_Trajectory.iterate import iterate_mdtraj_trajectory
#from molsysmt._private.exceptions import NotImplementedIteratorError
#from molsysmt._private.exceptions import IteratorError

class Iterator():
    """ A class that allows to iterate trough trajectories of any type.
    """
    def __init__(self,
                 molecular_system,
                 element = 'structure',
                 selection = 'all',
                 start = 0,
                 stop = None,
                 step = 1,
                 chunk = 1,
                 structure_indices = None,
                 syntaxis = "MolSysMT"
                 ):

        self.molecular_system = molecular_system
        self.element = element
        self.atom_indices = select(molecular_system, selection=selection, syntax=syntax)
        self.start = start
        self.stop = stop
        self.step = step
        self.chunk = chunk
        self.structure_indices = structure_indices

        self.position = 0

        self._iterators = []

        form_in = get_form(molecular_system)

        if not isinstance(form_in, [list, tuple]):
            self._iterators += dict_iterator[form_in]
        else:
            for aux_form in form_in:
                self._iterators += dict_iterator[aux_form]

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

