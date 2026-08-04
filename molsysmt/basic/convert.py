from molsysmt._private.smonitor import NotImplementedConversionError
from molsysmt._private.smonitor import NotCompatibleConversionError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt.configure import default_attribute
import inspect
import numpy as np

def _convert_one_to_one(molecular_system,
                        from_form,
                        to_form='molsysmt.MolSys',
                        selection='all',
                        structure_indices='all',
                        syntax='MolSysMT',
                        **kwargs):
    """Internal helper: convert a single input from one form to another (one-to-one path)."""

    from . import select, get_form
    from molsysmt.form import is_item, is_file, _dict_modules
    from molsysmt.element import _element_indices, _element_index
    from molsysmt.basic import has_attribute
    from molsysmt.attribute import attributes as _attributes

    output = None

    # Conversion arguments

    conversion_arguments={}

    # If to_form is a file

    output_is_file=False

    if is_item(to_form):
        if is_file(to_form):
            output_is_file=True
            conversion_arguments['output_filename'] = to_form
            to_form = get_form(to_form)

    # Straight conversion

    if to_form in _dict_modules[from_form]._convert_to:

        function = _dict_modules[from_form]._convert_to[to_form]

        if isinstance(function, str):
            from importlib import import_module
            # Load the submodule explicitly. e.g., molsysmt.form.file_pdb.to_molsysmt_Topology
            module_name = f"{_dict_modules[from_form].__name__}.{function}"
            module = import_module(module_name)
            # Get the function from the module (it has the same name as the module file)
            function = getattr(module, function)

        input_arguments = set(inspect.signature(function).parameters)

        if 'structure_indices' in input_arguments:
            conversion_arguments['structure_indices']=structure_indices

        for element, element_index in _element_index.items():
            if _element_indices[element] in input_arguments:
                if not is_all(selection):
                    conversion_arguments[_element_indices[element]] = select(molecular_system, element=element,
                                                                             selection=selection, syntax=syntax,
                                                                             skip_digestion=True)
                else:
                    conversion_arguments[_element_indices[element]] = 'all'
                break

        kwargs['skip_digestion']=True

        missing_arguments = input_arguments - (set(conversion_arguments) | set(kwargs) | {'item',
            'copy_if_all'})

        for missing_argument in missing_arguments:
            if missing_argument in default_attribute:
                kwargs[missing_argument]=default_attribute[missing_argument]

        missing_arguments = input_arguments - (set(conversion_arguments) | set(kwargs) | {'item',
        'copy_if_all'})

        if 'get_missing_bonds' in kwargs and 'get_missing_bonds' not in input_arguments:
            del kwargs['get_missing_bonds']


        if len(missing_arguments)>0:

            if hasattr(_dict_modules[from_form], '_conversion_opt_kwargs'):
                if to_form in _dict_modules[from_form]._conversion_opt_kwargs:
                    for opt_kwarg in _dict_modules[from_form]._conversion_opt_kwargs[to_form]:
                        if opt_kwarg in missing_arguments:
                            missing_arguments.discard(opt_kwarg)

            missing_arguments.discard('compression')
            missing_arguments.discard('compression_opts')
            missing_arguments.discard('int_precision')
            missing_arguments.discard('float_precision')
            missing_arguments.discard('get_missing_bonds')

            if len(missing_arguments)>0:
                raise NotCompatibleConversionError(from_form, to_form, missing_arguments)

        output = function(molecular_system, **conversion_arguments, **kwargs)

    elif ('molsysmt.MolSys' in _dict_modules[from_form]._convert_to) and (to_form in _dict_modules['molsysmt.MolSys']._convert_to):

        intermediate_function = _dict_modules[from_form]._convert_to['molsysmt.MolSys']
        if isinstance(intermediate_function, str):
            from importlib import import_module
            module_name = f"{_dict_modules[from_form].__name__}.{intermediate_function}"
            module = import_module(module_name)
            intermediate_function = getattr(module, intermediate_function)

        intermediate_signature = inspect.signature(intermediate_function)
        accepts_arbitrary_kwargs = any(
            parameter.kind is inspect.Parameter.VAR_KEYWORD
            for parameter in intermediate_signature.parameters.values()
        )
        if accepts_arbitrary_kwargs:
            intermediate_kwargs = kwargs
        else:
            intermediate_kwargs = {
                key: value
                for key, value in kwargs.items()
                if key in intermediate_signature.parameters
            }

        output = _convert_one_to_one(molecular_system, from_form, to_form='molsysmt.MolSys', selection=selection,
                structure_indices=structure_indices, syntax=syntax, **intermediate_kwargs)
        output = _convert_one_to_one(output, 'molsysmt.MolSys', to_form=to_form, **kwargs)

    return output


def _convert_multiple_to_one_with_shortcuts(molecular_system,
                                            from_forms,
                                            to_form='molsysmt.MolSys',
                                            selection='all',
                                            structure_indices='all',
                                            syntax='MolSysMT',
                                            **kwargs):
    """Internal helper: convert a list/tuple of inputs to one output using conversion shortcuts."""

    from . import select, get_form
    from molsysmt.form import is_item, is_file, _dict_modules
    from molsysmt.element import _element_indices, _element_index
    from molsysmt._private.conversion_shortcuts import _multiple_conversion_shortcuts
    from molsysmt.basic import has_attribute
    from molsysmt.attribute import attributes as _attributes

    output = None

    n_items = len(from_forms)

    # Conversion arguments

    conversion_arguments={}

    # If to_form is a file

    output_is_file=False

    if is_item(to_form):
        if is_file(to_form):
            output_is_file=True
            conversion_arguments['output_filename'] = to_form
            to_form = get_form(to_form)

    # Conversion 
    sorted_forms = tuple(sorted(from_forms))

    from molsysmt._private.conversion_shortcuts import _multiple_conversion_shortcuts

    if to_form in _multiple_conversion_shortcuts[sorted_forms]:
        function = _multiple_conversion_shortcuts[sorted_forms][to_form]

        input_arguments = set(inspect.signature(function).parameters)

        if 'structure_indices' in input_arguments:
            conversion_arguments['structure_indices']=structure_indices

        if 'get_missing_bonds' in kwargs and 'get_missing_bonds' not in input_arguments:
            del kwargs['get_missing_bonds']

        for element, element_index in _element_index.items():
            if _element_indices[element] in input_arguments:
                if not is_all(selection):
                    conversion_arguments[_element_indices[element]] = select(molecular_system, element=element,
                                                                             selection=selection, syntax=syntax,
                                                                             skip_digestion=True)
                else:
                    conversion_arguments[_element_indices[element]] = 'all'
                break

        output = function(molecular_system, **conversion_arguments, **kwargs)

    elif ('molsysmt.MolSys' in _multiple_conversion_shortcuts[sorted_forms]) and (to_form in _dict_modules['molsysmt.MolSys']._convert_to):
        output = _convert_multiple_to_one_with_shortcuts(molecular_system, sorted_forms, to_form='molsysmt.MolSys', selection=selection,
                structure_indices=structure_indices, syntax=syntax, **kwargs)
        output = _convert_one_to_one(output, 'molsysmt.MolSys', to_form=to_form)

    return output

def _prune_structural_attributes_off_the_axis(molecular_system, from_forms, from_attributes):
    """Removing structural attributes from items that do not span the structure axis.

    An item holding a single reference conformation beside a trajectory contributes
    identity and topology, not structures. Leaving its structural series in place would
    let item order decide how many structures the converted system has.
    """

    import warnings

    from molsysmt.attribute import is_structural_attribute
    from molsysmt._private.smonitor import StructuralAttributeOffAxisWarning
    from molsysmt._private.structure_axis import structure_axis

    axis, counts = structure_axis(molecular_system, from_forms, caller='molsysmt.convert')
    if axis is None:
        return

    dropped = set()
    for index, count in enumerate(counts):
        if count is None or count == axis:
            continue
        off_axis = {attribute for attribute in from_attributes[index]
                    if is_structural_attribute(attribute) and not attribute.startswith('n_')}
        from_attributes[index] -= off_axis
        dropped |= off_axis

    # Only report what no item on the axis can supply: otherwise the attribute is
    # delivered, just by the trajectory instead of by the reference conformation.
    on_axis = set()
    for index, count in enumerate(counts):
        if count == axis:
            on_axis |= from_attributes[index]
    dropped -= on_axis

    if dropped:
        warnings.warn(
            StructuralAttributeOffAxisWarning(attributes=sorted(dropped),
                                              caller='molsysmt.convert'),
            stacklevel=2,
        )


def _convert_multiple_to_one(molecular_system,
                             from_forms,
                             to_form='molsysmt.MolSys',
                             selection='all',
                             structure_indices='all',
                             syntax='MolSysMT',
                             **kwargs):
    """Internal helper: convert a list/tuple of inputs to one output via plain graph resolution."""

    from . import select, get_form
    from molsysmt.form import is_item, is_file, _dict_modules
    from molsysmt.element import _element_indices, _element_index
    from molsysmt._private.conversion_shortcuts import _multiple_conversion_shortcuts
    from molsysmt.basic import has_attribute
    from molsysmt.attribute import attributes as _attributes

    n_items = len(from_forms)

    # Conversion arguments

    conversion_arguments={}

    # If to_form is a file

    output_is_file=False

    if is_item(to_form):
        if is_file(to_form):
            output_is_file=True
            conversion_arguments['output_filename'] = to_form
            to_form = get_form(to_form)

    #### Checking attributes sets for straight and indirect conversion

    to_attributes = set([ii for ii,jj in _dict_modules[to_form].attributes.items() if jj])

    from_attributes = []
    for from_form, from_item in zip(from_forms, molecular_system):
        aux_set = set()
        for ii,jj in _dict_modules[from_form].attributes.items():
            if jj:
                if _dict_modules[from_form].has_attribute(from_item, ii):
                    aux_set.add(ii)
        from_attributes.append(aux_set)

    # Only items spanning the structure axis of the system may contribute structural
    # attributes. Pruning them here, once, keeps the three provider searches below --
    # which all walk the items from last to first -- from choosing a reference
    # conformation over the trajectory just because it was listed later.
    _prune_structural_attributes_off_the_axis(molecular_system, from_forms, from_attributes)

    attributes_to_be_discarded = []
    for attribute in to_attributes:
        if attribute.startswith('n_'):
            attributes_to_be_discarded.append(attribute)
    for attributes in from_attributes:
        for attribute in attributes:
            if attribute.startswith('n_'):
                attributes_to_be_discarded.append(attribute)

    attributes_to_be_discarded += ['box_volume', 'box_shape', 'box_angles', 'box_lengths']
    attributes_to_be_discarded += ['atom_index', 'structure_index']

    for attribute in attributes_to_be_discarded:
        to_attributes.discard(attribute)
        for ii in from_attributes:
            ii.discard(attribute)

    all_from_attributes = set()
    all_from_attributes = all_from_attributes.union(*from_attributes)

    #### straight conversion

    straight_conversions = {}

    for item_index in range(n_items):
        from_form = from_forms[item_index]
        aux_set = from_attributes[item_index]
        if from_form in _dict_modules:
            if to_form in _dict_modules[from_form]._convert_to:

                function = _dict_modules[from_form]._convert_to[to_form]

                if isinstance(function, str):
                    from importlib import import_module
                    module_name = f"{_dict_modules[from_form].__name__}.{function}"
                    module = import_module(module_name)
                    function = getattr(module, function)

                input_arguments = set(inspect.signature(function).parameters)
                for ii in ['atom_indices', 'group_indices', 'component_indices', 'chain_indices',
                        'molecule_indices', 'entity_indices', 'structure_indices', 'molecular_system',
                        'copy_if_all']:
                    input_arguments.discard(ii)

                attributes_in_other_forms = {}

                for aux_attribute in (all_from_attributes - aux_set) & to_attributes:
                    for ii in range(n_items-1,-1,-1):
                        if aux_attribute in from_attributes[ii]:
                            attributes_in_other_forms[aux_attribute]=[molecular_system[ii], from_forms[ii]]
                            break

                repeated_attributes = {}
                for aux_attribute in aux_set:
                    for ii in range(n_items-1, item_index, -1):
                        if aux_attribute in from_attributes[ii]:
                            if has_attribute(molecular_system[ii], aux_attribute):
                                repeated_attributes[aux_attribute]=[molecular_system[ii], from_forms[ii]]
                                break

                input_attributes = {}
                set_attributes = {}

                for aux_attribute, aux_value in attributes_in_other_forms.items():
                    if _dict_modules[from_form].attributes[aux_attribute]:
                        set_attributes[aux_attribute]=aux_value
                    else:
                        if aux_attribute in input_arguments:
                            input_attributes[aux_attribute]=aux_value
                        else:
                            set_attributes[aux_attribute]=aux_value

                for aux_attribute, aux_value in repeated_attributes.items():
                    set_attributes[aux_attribute]=aux_value

                status_input_attributes = True
                status_set_attributes = True

                for aux_attribute in set_attributes:
                    set_to = _attributes[aux_attribute]['set_to']
                    if not hasattr(_dict_modules[to_form], f'set_{aux_attribute}_to_{set_to}'):
                        status_set_attributes = False
                        break


                straight_conversions[item_index] = {
                        'item' : molecular_system[item_index],
                        'form' : from_form,
                        'input_arguments' : input_arguments,
                        'attributes_in_form' : aux_set,
                        'attributes_in_other_forms': attributes_in_other_forms,
                        'repeated_attributes': repeated_attributes,
                        'input_attributes': input_attributes,
                        'set_attributes': set_attributes,
                        'status_set_attributes': status_set_attributes,
                        }

    if False:
        for ii in straight_conversions:
            print(ii, straight_conversions[ii])
            print('----')
        print('@@@@')

    basic_index = None
    n_set_attributes = np.inf

    for aux_index, aux_dict in straight_conversions.items():
        if aux_dict['status_set_attributes']:
            if n_set_attributes > len(aux_dict['set_attributes']):
                basic_index = aux_index
                n_set_attributes = len(aux_dict['set_attributes'])

    if basic_index is not None:

        aux_dict = straight_conversions[basic_index]

        for aux_attribute, aux_item_form in aux_dict['input_attributes'].items():
            aux_item = aux_item_form[0]
            aux_form = aux_item_form[1]
            get_from = _attributes[aux_attribute]['get_from'][0]
            get_function = getattr(_dict_modules[aux_form], f'get_{aux_attribute}_from_{get_from}')
            get_arguments = {}
            input_arguments = set(inspect.signature(get_function).parameters)
            if 'structure_indices' in input_arguments:
                get_arguments['structure_indices']=structure_indices
            if 'indices' in input_arguments:
                if not is_all(selection):
                    get_arguments['indices'] = select(molecular_system, element=get_from, selection=selection,
                                                      syntax=syntax, skip_digestion=True)
                else:
                    get_arguments['indices'] = 'all'
            conversion_arguments[aux_attribute] = get_function(aux_item, **get_arguments)
        conversion_function = _dict_modules[aux_dict['form']]._convert_to[to_form]

        if isinstance(conversion_function, str):
            from importlib import import_module
            module_name = f"{_dict_modules[aux_dict['form']].__name__}.{conversion_function}"
            module = import_module(module_name)
            conversion_function = getattr(module, conversion_function)

        input_arguments = set(inspect.signature(conversion_function).parameters)
        if 'structure_indices' in input_arguments:
            conversion_arguments['structure_indices']=structure_indices
        for element, element_index in _element_index.items():
            if _element_indices[element] in input_arguments:
                if not is_all(selection):
                    conversion_arguments[_element_indices[element]] = select(molecular_system, element=element,
                                                                             selection=selection, syntax=syntax,
                                                                             skip_digestion=True)
                else:
                    conversion_arguments[_element_indices[element]] = 'all'
                break
        output = conversion_function(aux_dict['item'], **conversion_arguments, **kwargs)

        for aux_attribute, aux_item_form in aux_dict['set_attributes'].items():
            aux_item = aux_item_form[0]
            aux_form = aux_item_form[1]
            get_from = _attributes[aux_attribute]['get_from'][0]
            get_function = getattr(_dict_modules[aux_form], f'get_{aux_attribute}_from_{get_from}')
            get_arguments = {}
            input_arguments = set(inspect.signature(get_function).parameters)
            if 'structure_indices' in input_arguments:
                get_arguments['structure_indices']=structure_indices
            if 'indices' in input_arguments:
                if not is_all(selection):
                    get_arguments['indices'] = select(molecular_system, element=get_from, selection=selection, syntax=syntax)
                else:
                    get_arguments['indices'] = 'all'
            value_to_set = get_function(aux_item, **get_arguments)
            if _set_composed_structure_attribute(
                output,
                aux_attribute,
                value_to_set,
            ):
                continue
            set_to = _attributes[aux_attribute]['set_to']
            set_function = getattr(_dict_modules[to_form], f'set_{aux_attribute}_to_{set_to}')
            set_function(output, value=value_to_set)

    elif to_form=='molsysmt.MolSys' and basic_index is None:

        print('The conversion needs to include new set functions:')

        for aux_index, aux_dict in straight_conversions.items():
            print('   ')
            print('To ', aux_dict['form'], ':')
            print('   ')
            for att, mm in aux_dict['set_attributes'].items():
                set_to = _attributes[att]['set_to']
                if not hasattr(_dict_modules[to_form], f'set_{att}_to_{set_to}'):
                    print(att, 'from', mm[1], 'to', set_to)


            print('   ')

        from molsysmt._private.smonitor import InternalAlgorithmError
        raise InternalAlgorithmError(
            reason="The conversion needs to include new set functions.",
            caller="molsysmt.basic.convert"
        )

    elif to_form!='molsysmt.MolSys':

        output = _convert_multiple_to_one(molecular_system, from_forms, to_form='molsysmt.MolSys', selection=selection,
                structure_indices=structure_indices, syntax=syntax, **kwargs)
        if output is not None:
            output = _convert_one_to_one(output, 'molsysmt.MolSys', to_form=to_form)

    if to_form == 'molsysmt.MolSys' and output is not None:
        _reconcile_composed_structure_state_association(output)

    return output


def _set_composed_structure_attribute(item, attribute, value):
    """Replace one complete structure-aligned series during composition."""

    canonical_units = {
        'time': 'ps',
        'coordinates': 'nm',
        'velocities': 'nm/ps',
        'box': 'nm',
        'b_factor': 'nm**2',
        'temperature': 'K',
        'potential_energy': 'kJ/mol',
        'kinetic_energy': 'kJ/mol',
    }
    structure_attributes = {
        'structure_id',
        'time',
        'coordinates',
        'velocities',
        'box',
        'b_factor',
        'alternate_location',
        'occupancy',
        'temperature',
        'potential_energy',
        'kinetic_energy',
    }
    if attribute not in structure_attributes:
        return False
    if value is None:
        return False

    from molsysmt.native import Structures

    if isinstance(item, Structures):
        structures = item
    elif hasattr(item, 'structures') and isinstance(item.structures, Structures):
        structures = item.structures
    else:
        return False

    if attribute in canonical_units:
        from molsysmt.native.structures import _raw_value

        value = _raw_value(value, canonical_units[attribute])

    candidate = structures._frame_payload()
    candidate[attribute] = value
    n_structures = len(value)
    for name, current in candidate.items():
        if current is not None and len(current) != n_structures:
            candidate[name] = None
    structures._assign_frame_payload(candidate)
    return True


def _reconcile_composed_structure_state_association(item):
    """Align explicit chemical-state associations after composite conversion."""

    explicit = item._structure_chemical_state_indices
    if explicit is None:
        return

    n_structures = item.structures.n_structures
    if len(explicit) == n_structures:
        return

    if len(item.topology._chemical_states) == 1:
        item._structure_chemical_state_indices = None
    else:
        import pandas as pd

        item._structure_chemical_state_indices = pd.array(
            [pd.NA] * n_structures,
            dtype='Int64',
        )

from smonitor import signal

@signal(tags=['api', 'conversion'])
@arg_digest()
def convert(molecular_system,
            to_form='molsysmt.MolSys',
            selection='all',
            structure_indices='all',
            syntax='MolSysMT',
            strict=False,
            return_report=False,
            skip_digestion=False,
            **kwargs):
    """
    Converting a molecular system into another form or set of forms.

    This function converts a molecular system from its current form into one target form, or into
    multiple target forms. Optionally, a subset of atoms and/or structures can be selected using
    `selection` and `structure_indices` before the conversion takes place.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system provided in any of the :ref:`supported forms <Introduction_Forms>`.
    to_form : str or list of str, default 'molsysmt.MolSys'
        Target form (or list of forms) for the conversion output. When a list is given,
        the function returns a list with one converted output per requested form.
        See :ref:`Supported conversions <Introduction_Supported>`.
    selection : str, tuple, list or numpy.ndarray, default 'all'
        Atom selection to apply prior to conversion. Either a 0-based index collection or a
        selection string parsed according to :ref:`Introduction_Selection`. The default 'all' includes
        the entire system.
    structure_indices : int, tuple, list, numpy.ndarray or 'all', default 'all'
        0-based indices of the structures to include in the conversion. The default 'all' includes all structures.
    syntax : str, default 'MolSysMT'
        Selection syntax used when `selection` is a string. See :ref:`Introduction_Selection`.
    strict : bool, default=False
        Whether to reject the conversion before execution when the semantic
        preflight identifies supplied semantics that the target cannot preserve.
    return_report : bool, default=False
        Whether to return an immutable :class:`molsysmt.ConversionReport`
        together with the converted object. The conversion preflight runs only
        when this option or `strict=True` requests it.
    skip_digestion : bool, default False
        Whether to skip MolSysMT’s internal argument digestion mechanism.

        MolSysMT includes a built-in digestion system that validates and normalizes
        function arguments. This process checks types, shapes, and values, and automatically
        adjusts them when possible to meet expected formats.

        Setting `skip_digestion=True` disables this process, which may improve performance
        in workflows where inputs are already validated. Use with caution: only set this to
        `True` if you are certain all input arguments are correct and consistent.
    **kwargs
        Additional keyword arguments forwarded to specific conversion handlers when required
        by a particular input-output path (e.g., topology or box handling options).

    Returns
    -------
    molecular system or list of molecular systems or tuple
        The converted molecular system in the requested `to_form`. If `to_form` is a list,
        a list of converted systems is returned. With `return_report=True`, returns
        ``(output, report)`` or ``(outputs, reports)`` for multiple targets.

    Raises
    ------
    NotSupportedFormError
        If the input system or the requested target form is not supported.
    NotCompatibleConversionError
        If `strict=True` and the preflight classifies the conversion as lossy.
    ArgumentError
        If any input argument is invalid or inconsistent, including an
        out-of-range structure index.

    Notes
    -----
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.
    - Explicit structure indices are validated before a conversion adapter is called.
    - Reports classify semantics only within their ``audited_scopes``. Inspect
      ``is_exhaustive`` before treating an ``equivalent`` outcome as a claim
      about the complete represented source state. Strict lossy conversions
      are rejected before target creation.
    - Missing source information is not a loss. A report issue is created only
      for an attribute available on the source instance or for an audited
      adapter limitation.
    - Ordinary conversions do not construct a preflight report. This keeps the
      reporting layer opt-in when neither `strict` nor `return_report` is used.

    See Also
    --------
    :func:`molsysmt.basic.select`
        Select elements of a molecular system.
    :func:`molsysmt.basic.get_form`
        Retrieve the form of a molecular system.
    :func:`molsysmt.basic.extract`
        Extract a subset of a molecular system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys_A = '2LAO'
    >>> msm.get_form(molsys_A)
    'string:pdb_id'
    >>> molsys_B = msm.convert(molsys_A, to_form='openmm.Topology')
    >>> msm.get_form(molsys_B)
    'openmm.Topology'
    >>> _, report = msm.convert(molsys_B, to_form='molsysmt.Topology', return_report=True)
    >>> report.outcome in {'exact', 'equivalent', 'lossy'}
    True

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Convert`.

    .. versionadded:: 1.0.0
    """

    from . import get_form
    from molsysmt._private.conversion_shortcuts import _multiple_conversion_shortcuts

    output = None

    from_form = get_form(molecular_system)

    if isinstance(from_form, (list, tuple)):
        if len(from_form)==1:
            molecular_system = molecular_system[0]
            from_form = from_form[0]

    from ._index_validation import validate_structure_indices

    structure_indices = validate_structure_indices(
        molecular_system, structure_indices, 'molsysmt.convert'
    )

    # If to_form is a list, convert is invoked iteratively

    if isinstance(to_form, (list, tuple)):
        output=[]
        reports=[]
        for item_out in to_form:
            converted = convert(
                molecular_system, to_form=item_out, selection=selection,
                structure_indices=structure_indices, syntax=syntax, strict=strict,
                return_report=return_report, skip_digestion=True, **kwargs
            )
            if return_report:
                item_output, item_report = converted
                output.append(item_output)
                reports.append(item_report)
            else:
                output.append(converted)
        return (output, reports) if return_report else output

    report = None
    if strict or return_report:
        from molsysmt._private.conversion_report import build_conversion_report

        report = build_conversion_report(
            molecular_system,
            from_form,
            to_form,
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
        )
        if strict and report.is_lossy:
            raise NotCompatibleConversionError(
                report.from_form,
                report.to_form,
                {issue.attribute for issue in report.issues},
                caller='molsysmt.convert',
                message=(
                    'Strict conversion rejected supplied semantics that the target '
                    f'cannot preserve: {[issue.attribute for issue in report.issues]}'
                ),
            )

    # If one to one
    if not isinstance(from_form, (list, tuple)):
        output = _convert_one_to_one(molecular_system, from_form, to_form=to_form, selection=selection, structure_indices=structure_indices,
                syntax=syntax, skip_digestion=True, **kwargs)

    # If multiple to one

    else:

        # conversions in private shortcuts
        if tuple(sorted(from_form)) in _multiple_conversion_shortcuts:
            output = _convert_multiple_to_one_with_shortcuts(molecular_system, from_form, to_form=to_form, selection=selection, structure_indices=structure_indices,
                syntax=syntax, skip_digestion=True, **kwargs)

        # general conversion
        if output is None:
            output = _convert_multiple_to_one(molecular_system, from_form, to_form=to_form, selection=selection, structure_indices=structure_indices,
                syntax=syntax, skip_digestion=True, **kwargs)

    # Returning the output

    if output is None:

        from_form = get_form(molecular_system)
        if len(from_form)==1:
            from_form=from_form[0]
        raise NotImplementedConversionError(from_form, to_form)

    if isinstance(output, (list, tuple)):
        if len(output) == 1:
            output = output[0]

    return (output, report) if return_report else output
