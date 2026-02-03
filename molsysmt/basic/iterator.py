from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.exceptions import NotImplementedIteratorError
#from molsysmt._private.exceptions import IteratorError

class Iterator():
    """
    Iterating over topological or structural attributes of a molecular system.

    This class provides a unified interface to iterate over selected attributes of a molecular
    system — either topological (e.g., `atom_name`, `group_index`) or structural (e.g., `coordinates`,
    `box`, `time`). Iteration proceeds over elements (atoms, groups, molecules, etc.) or over
    structures depending on the requested attributes. When no attributes are requested, each
    iteration yields a molecular system with updated structural data (trajectory-like behavior).

    Parameters
    ----------
    (see __init__)

    Attributes
    ----------
    molecular_system : molecular system
        Molecular system from which attribute values are extracted.
    element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'}
        Hierarchical level over which iteration is performed.
    indices : int, list, tuple or numpy.ndarray
        Element indices used for iteration (as resolved from `selection`).
    structure_indices : int, list, tuple or numpy.ndarray
        Structure indices used when iterating over structural attributes.
    start, stop, step, chunk : int
        Control parameters defining the iteration window and stride.
    iterator_index : int
        Current iteration position.
    arguments : list of str
        Attribute names returned on each iteration.

    Notes
    -----
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.
    - This class implements the Python iterator protocol:
      `__iter__()` returns `self`, and `__next__()` returns the next item or raises `StopIteration`.
    - If no attributes are requested, the iterator returns a molecular system per iteration
    with updated structural attributes.

    See Also
    --------
    :func:`molsysmt.basic.select` :
        Select elements from a molecular system.
    :func:`molsysmt.basic.get` :
        Retrieve values of attributes from a molecular system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> molsys = systems['chicken villin HP35']['1vii.bcif.gz']
    >>> it1 = msm.Iterator(molsys, element='group', selection='molecule_type=="peptide"',
    ...                    start=10, stop=20, step=2, group_index=True, group_name=True)
    >>> for group_index, group_name in it1:
    ...     pass # replace with desired operations
    >>> molsys = systems['pentalanine']['traj_pentalanine.h5']
    >>> it2 = msm.Iterator(molsys, selection='group_index==3 and atom_name=="CA"',
    ...                    structure_indices=[100, 110, 120],
    ...                    time=True, coordinates=True)
    >>> for time, coordinates in it2:
    ...     pass # replace with desired operations

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this class,
       along with additional examples:
       :ref:`Tutorial_Iterator`.

    .. versionadded:: 1.0.0
    """

    @arg_digest()
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
                 skip_digestion = False,
                 **kwargs,
                 ):
        """
        Initializing an iterator over attributes of a molecular system.

        Parameters
        ----------
        molecular_system : molecular system
            Input system in any of the :ref:`supported forms <Introduction_Forms>`.
        element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'}, default 'atom'
            Hierarchical level guiding selection and topological iteration.
        selection : int, index, tuple, list, numpy.ndarray or str, default 'all'
            Elements to iterate over. Indices or a selection string (see :ref:`Introduction_Selection`).
        structure_indices : int, list, tuple, numpy.ndarray or 'all', optional
            Structure indices (0-based) used if **all** requested attributes are structural.
        start, stop, step, chunk : int, default (0, None, 1, 1)
            Iteration control parameters:
            - `start`: starting position
            - `stop`: final exclusive position (``None`` means until the end)
            - `step`: stride between positions
            - `chunk`: number of positions advanced per yielded item
        syntax : str, default 'MolSysMT'
            Selection syntax used when `selection` is a string. See :ref:`Introduction_Selection`.
        output_type : {'values', 'dictionary'}, default 'values'
            Format of the returned item when attributes are requested:
            - `'values'`: tuple with atribute values in order (or a single value if only one attribute)
            - `'dictionary'`: mapping `{attribute_names: keys}`
        output_form : str, default 'molsysmt.MolSys'
            Form of the yielded molecular system when no attributes are requested.
        **kwargs : {str: bool}
            Attributes to extract (e.g., `time=True`, `coordinates=True`). Keys must be valid
            attribute names; only those with `True` are included.

        Raises
        ------
        NotSupportedFormError
            If the input system has an unsupported form.
        ArgumentError
            If any input argument is invalid or inconsistent.
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
        Returning the iterator object.

        This method returns `self` to enable usage in `for` loops and other iteration
        contexts.

        Returns
        -------
        molsysmt.basic.Iterator
            The iterator instance itself.
        """

        return self

    def __next__(self):
        """
        Producing the next item in the iteration.

        If attributes were requested in `**kwargs`, this method returns either a tuple of
        values (`output_type='values'`) or a dictionary of `{attribute_name: value}`
        (`output_type='dictionary'`). If no attributes were requested, it returns a
        molecular system in `output_form` whose structural data (`structure_id`, `time`,
        `coordinates`, `box`) are updated to the current iteration.

        Returns
        -------
        Any
            Tuple, single value, dictionary, or a molecular system depending on the
            initialization parameters (see above).

        Raises
        ------
        StopIteration
            When no further items are available.
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

