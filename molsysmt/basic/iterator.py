from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedIteratorError
#from molsysmt._private.exceptions import IteratorError

class Iterator():
    """
    Iterator over attributes of a molecular system.

    This class is an iterator over specific topological or structural attributes of a molecular
    system. As any iterator, the class contains two privated methods which makes the class
    functional in this context: ``__iter__`` and ``__next__`` (see :ref:`notes`).  New objects can be
    instanstiated specifying the set of attributes to be extracted in each iteration, as well as
    the selection of elements to get those attributes, and some input parameters to control the
    iterations.


    Attributes
    ----------

    molecular_system: molecular system
        The molecular system whose attributes are extracted by the iterator.

    element: {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'}
        The iterator extracts specific molecular systems attribute values in each iteration for a set of elements
        defined by this attribute and the ``indices`` attribute.

    indices: int, list, tuple, numpy.ndarray
        Elements indices the iterator uses to extract the molecular systems attributes in each
        iteration.

    structure_indices: int, list, tuple, numpy.ndarray
        Structure indices the iterator uses in case structural attributes are extracted in each
        iteration.

    start: int
        Attribute to store the initial interation index.

    stop: int
        Attribute to store the final iteration index.

    step: int
        Attribute to store the iteration step -increment-.

    chunk: int
        Number of of steps -increments- effectively done by interation.

    iterator_index: int
        Attribute to store the current interation index.

    arguments: list
        List of molecular systems attributes to be extracted in each iteration.



    .. versionadded:: 0.7.0


    .. _notes:

    Notes
    -----

    The class works as iterator thanks to the following private methods:

    - :func:`__iter__`
        The private method :func:`__iter__` returns the `self` variable to make this class working
        as an interator. It must be invoked with out any input argument.

    - :func:`__next__`
        The private method :func:`__next__` returns the values of the molecular
        systems' attributes corresponding to the next iteration. It must be invoked with out any
        input argument.

    The list of supported molecular systems' forms is detailed in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.

    The list of supported selection syntaxes can be checked in the documentation section
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`.

    The list of supported selection syntaxes can be checked in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Attributes <Introduction_Attributes>`.


    See Also
    --------

    :func:`molsysmt.basic.select`
        Selecting elements of a molecular system

    :func:`molsysmt.basic.get`
        Getting attributes of a molecular system

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
        Instantation method of the iterator.

        The following parameters need to be introduced as input arguments to instante new
        iterators.

        The resultant object can be used to iterate over specific topological or structural
        attributes of a molecular system. The set of attributes to be extracted in each iteration,
        as well as the selection of elements to get those attributes, and some input parameters to
        control the iterations, have to be specified with these arguments.


        Parameters
        ----------

        molecular_system: molecular system
            The molecular system in any of :ref:`the supported forms
            <Introduction_Forms>`, whose attributes are extracted by the iterator.

        element: {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'}, default 'atom'
            The iterator extracts specific attribute values in each iteration for a set of elements
            defined by this attribute and the ``selection`` input argument.

        selection : index, tuple, list, numpy.ndarray or str, default 'all'
            Selection of elements of the molecular system to get the required attributes. The
            selection can be given by a list, tuple or numpy array of element indices (0-based
            integers) -up to the value of the ``element`` input argument-; or by means of a query
            string following any of :ref:`the selection syntaxes parsable by MolSysMT
            <Introduction_Selection>`.

        structure_indices : integer, tuple, list, numpy.ndarray or 'all', default 'all'
            Indices of structures (0-based integers) to be used by the iterator in case structural
            attributes are extracted in each iteration.

        start: int, default 0
            Initial interation index.

        stop: int, None, default None
            Final iteration index. If None (default), the iterator runs as long as it is possible.

        step: int, default 1
            Iteration step -increment-.

        chunk: int, default 1
            Number of of steps -increments- effectively done by interation.

        syntax : str, default 'MolSysMT'
            :ref:`Supported syntax <Introduction_Selection>` used in the `selection` argument (in case
            it is a string).

        output_type: {'values', 'dictionary'}, default 'values'
            If 'values', the list of attribute values are returned in the same
            order they were required every iteration step. With 'dictionary' a dictionary is returned
            with the attribute names as keys, and corresponding attribute values as
            values.

        output_form: 'molsysmt.MolSys'
            If no attributes are required (``**kwargs=None``), a molecular system is returned every
            iteration step with the structural attributes such as coordinates, box, step, and time,
            updated. This input argument defines the form of the resultant molecular system.

        **kwargs : {{keyword : str,  value : bool}, default None}
            The attributes required are introduced as additional keywords with value 'True'
            if their value needs to be extracted by the iterator.


        Returns
        -------
        molsysmt.basic.iterator.Iterator
            The function returns an Iterator object of this class. This object can be used as
            iterator and the required attribute values as a list will be returned in each iteration
            step if the input argument ``output_type`` takes the value 'values'; or together with
            the attribute names in a dictionary if the argument ``output_type`` takes the value
            'dictionary'. If a required attribute is not found in the form of the input molecular
            system, the function assigns None as returned value.


        Raises
        ------

        NotSupportedFormError
            The function raises a NotSupportedFormError in case a molecular system
            is introduced with a not supported form.

        ArgumentError
            The function raises an ArgumentError in case an input argument value
            does not meet the required conditions.

        SyntaxError
            The function raises a SyntaxError in case the syntax argument takes a not supported value.


        Examples
        --------

        The following example illustrates the use of this class to iterate over topological attributes.

        >>> import molsysmt as msm
        >>> molecular_system = msm.systems.demo['chicken villin HP35']['1vii.mmtf']
        >>> iterator = msm.Iterator(molecular_system, element='group', selection='molecule_type=="protein"', start=10, stop=20, step=2,
        >>>                         group_index=True, group_name=True, formal_charge=True)
        >>> for group_index, group_name, formal_charge in iterator:
        >>>     print(group_index, group_name, formal_charge)
        10 PHE 0.0 elementary_charge
        12 MET 0.0 elementary_charge
        14 ARG 1.0 elementary_charge
        16 ALA 0.0 elementary_charge
        18 ALA 0.0 elementary_charge


        This other example illustrates the use of this class to iterate over structural attributes.

        >>> import molsysmt as msm
        >>> molecular_system = msm.systems.demo['pentalanine']['traj_pentalanine.h5']
        >>> iterator = msm.Iterator(molecular_system, selection='group_index==3 and atom_name=="CA"',
        >>>                         structure_indices=[100, 110, 120], time=True, coordinates=True)
        >>> for time, coordinates in iterator:
        >>>     print(time, coordinates)
        1010.0 picosecond [[[0.9690295457839966 1.146891474723816 -0.1522401124238968]]] nanometer
        1110.0 picosecond [[[1.023858666419983 1.377505898475647 0.03329920768737793]]] nanometer
        1210.0 picosecond [[[0.9038813710212708 1.1570117473602295 0.03575613722205162]]] nanometer


        .. admonition:: User guide

           Follow this link for a tutorial on how to work with this function:
           :ref:`User Guide > Tools > Basic > Iterator <Tutorial_Iterator>`.


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

