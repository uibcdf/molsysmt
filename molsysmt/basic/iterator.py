from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedIteratorError
#from molsysmt._private.exceptions import IteratorError

class Iterator():
    """
    Iterate over topological or structural attributes of a molecular system.

    This class provides a unified interface to iterate over selected attributes of a molecular
    system — either topological (e.g., `atom_name`, `group_index`) or structural (e.g., `coordinates`, `box`, `time`).
    Iteration is element-based (atoms, groups, molecules, etc.) or structure-based depending on the attributes requested.

    The class supports standard iterator behavior via the `__iter__()` and `__next__()` methods (see :ref:`notes`).
    It is instantiated with a set of arguments defining the target attributes, selection criteria, and iteration control.

    Attributes
    ----------
    molecular_system : molecular system
        The molecular system from which attribute values are extracted.

    element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'}
        Type of elements over which the iteration is performed.

    indices : int, list, tuple, or numpy.ndarray
        Indices of elements (e.g., atoms or groups) to iterate over.

    structure_indices : int, list, tuple, or numpy.ndarray
        Indices of structures to be used if iterating over structural attributes.

    start, stop, step, chunk : int
        Control parameters that define how the iteration proceeds.

    iterator_index : int
        Current index in the iteration.

    arguments : list
        List of attributes to be returned on each iteration.

    Notes
    -----
    This class is a Python iterator and implements:

    - `__iter__()`: returns `self`, enabling use in loops.
    - `__next__()`: returns the next attribute values, or raises `StopIteration`.

    If no attributes are requested, the iterator returns a molecular system per iteration
    with updated structural attributes.

    See also:
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`  
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`  
    :ref:`User Guide > Introduction > Molecular systems > Attributes <Introduction_Attributes>`

    See Also
    --------
    :func:`molsysmt.basic.select`
        Selecting elements of a molecular system.

    :func:`molsysmt.basic.get`
        Getting attribute values from a molecular system.

    .. versionadded:: 1.0.0
    """

    @digest()
    def __init__(self,
                 molecular_system,
                 element = 'atom',
                 selection = 'all',
                 structure_indices = None,
                 start = 0,
                 stop = None,
                 step = 1,
                 chunk = 1,
                 syntax = 'MolSysMT',
                 output_type = 'values',
                 output_form = 'molsysmt.MolSys',
                 **kwargs,
                 ):
        """
        Initialize a new Iterator instance.

        Parameters
        ----------
        molecular_system : molecular system
            A molecular system in any of the :ref:`supported forms <Introduction_Forms>`.

        element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'}, default 'atom'
            The element type over which the iteration is performed.

        selection : index, tuple, list, numpy.ndarray or str, default 'all'
            Selection of elements to iterate over. Can be given as indices or a selection string.
            See: :ref:`Introduction_Selection`.

        structure_indices : int, list, tuple, numpy.ndarray or 'all', default 'all'
            Indices of structures (0-based) to be used if structural attributes are selected.

        start, stop, step, chunk : int
            Iteration control:
            - `start`: starting index (default 0)
            - `stop`: final index (default: as far as possible)
            - `step`: increment between steps (default 1)
            - `chunk`: number of steps per iteration (default 1)

        syntax : str, default 'MolSysMT'
            Selection syntax (if `selection` is a string).

        output_type : {'values', 'dictionary'}, default 'values'
            Output format:
            - `'values'`: tuple with attribute values in order
            - `'dictionary'`: dict with attribute names as keys

        output_form : str, default 'molsysmt.MolSys'
            Form of returned molecular system if no attributes are requested.

        **kwargs : {str: bool}, optional
            Attributes to be extracted. Each keyword must be a valid attribute name, with `True` to include it.

        Returns
        -------
        molsysmt.basic.Iterator
            An instance of the `Iterator` class, ready to be used in a loop.

        Raises
        ------
        NotSupportedFormError
            If the input system has an unsupported form.

        ArgumentError
            If any input argument is invalid or inconsistent.

        SyntaxError
            If the `syntax` string is not recognized.

        Examples
        --------
        >>> import molsysmt as msm
        >>> molsys = msm.systems['chicken villin HP35']['1vii.bcif.gz']
        >>> iterator = msm.Iterator(molsys, element='group', selection='molecule_type=="protein"',
        ...                         start=10, stop=20, step=2,
        ...                         group_index=True, group_name=True, formal_charge=True)
        >>> for group_index, group_name, formal_charge in iterator:
        ...     print(group_index, group_name, formal_charge)

        >>> molsys = msm.systems['pentalanine']['traj_pentalanine.h5']
        >>> iterator = msm.Iterator(molsys, selection='group_index==3 and atom_name=="CA"',
        ...                         structure_indices=[100, 110, 120],
        ...                         time=True, coordinates=True)
        >>> for time, coordinates in iterator:
        ...     print(time, coordinates)

        .. admonition:: User guide

           Follow this link for a tutorial on how to use this class:
           :ref:`User Guide > Tools > Basic > Iterator <Tutorial_Iterator>`
        """

        from . import select, get_form, where_is_attribute, convert
        from molsysmt.attribute import is_structural_attribute
        from molsysmt.form import _dict_modules

        self.molecular_system = molecular_system
        self.element = element
        self.indices = select(molecular_system, element=element, selection=selection, syntax=syntax)
        self.structure_indices = structure_indices
        self.start = start
        self.stop = stop
        self.step = step
        self.chunk = chunk
        self.iterator_index = 0

        self.arguments = []

        self._iterators = []
        self._output_dictionary = {}
        self._output_type = output_type
        self._output_form= output_form
        self._output_molecular_system = None

        for ii, key in enumerate(kwargs.keys()):
            if kwargs[key]:
                self.arguments.append(key)

        if len(self.arguments)==0:
            self.arguments = ['structure_id', 'time', 'coordinates', 'box']
            self._output_molecular_system = convert(self.molecular_system, selection=selection,
                    structure_indices=None, to_form=self._output_form)

        self._output_dictionary = {ii:None for ii in self.arguments}

        aux_items_forms = {}
        aux_items_arguments = {}

        for argument in self.arguments:
            item, form = where_is_attribute(self.molecular_system, argument)
            if item in aux_items_forms:
                aux_items_arguments[item].append(argument)
            else:
                aux_items_forms[item]=form
                aux_items_arguments[item]=[argument]

        runs_in_structures = False
        if all([is_structural_attribute(ii) for ii in self.arguments]):
            runs_in_structures = True

        for item in aux_items_forms:

            tmp_arguments = {ii:True for ii in aux_items_arguments[item]}

            if runs_in_structures:
                if item is not None:
                    tmp_iterator = _dict_modules[aux_items_forms[item]].StructuresIterator(item, atom_indices=self.indices, start=self.start,
                       stop=self.stop, step=self.step, chunk=self.chunk, structure_indices=self.structure_indices, output_type='dictionary',
                       **tmp_arguments)
            else:
                tmp_iterator = _dict_modules[aux_items_forms[item]].TopologyIterator(item, element=self.element, indices=self.indices, start=self.start,
                       stop=self.stop, step=self.step, chunk=self.chunk, output_type='dictionary',
                       **tmp_arguments)

            self._iterators.append(tmp_iterator)

        del(aux_items_forms, aux_items_arguments)

    def __iter__(self):
        """
        Iterator private method

        This method returns the `self` variable to make this class working
        as an interator. It must be invoked with out any input argument.
        """

        return self

    def __next__(self):
        """
        Iterator private method

        This method returns the values of the molecular systems' attributes corresponding to the
        next iteration. It must be invoked with out any input argument.
        """

        try:

            for iterator in self._iterators:

                self._output_dictionary.update(iterator.__next__())

        except:

            raise StopIteration

        if self._output_molecular_system is None:
            if self._output_type=='values':
                output = list(self._output_dictionary.values())
                if len(output) == 1:
                    output = output[0]
            elif self._output_type=='dictionary':
                output = self._output_dictionary
            return  output
        else:
            from . import set
            set(self._output_molecular_system, element='atom', coordinates=self._output_dictionary['coordinates'])
            set(self._output_molecular_system, element='system', box=self._output_dictionary['box'],
                    structure_id=self._output_dictionary['structure_id'], time=self._output_dictionary['time'])
            return self._output_molecular_system

