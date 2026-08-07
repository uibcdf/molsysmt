from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all, is_iterable_of_iterables
import numpy as np

from smonitor import signal
from molsysmt._private.chemical_state import resolve_chemical_state

@signal(tags=['api', 'get'])
@arg_digest()
@resolve_chemical_state
def get(molecular_system,
        element='system',
        selection='all',
        structure_indices='all',
        mask=None,
        syntax='MolSysMT',
        get_missing_bonds=True,
        output_type='values',
        chemical_state='reference',
        skip_digestion=False,
        **kwargs):
    """
    Retrieving attribute values from a molecular system.

    This function retrieves values of one or more attributes from a molecular system (or from
    a selected subset of it), optionally specifying the hierarchical `element` level. Attributes
    to be returned are indicated via keyword flags in `**kwargs` (e.g., ``n_atoms=True``,
    ``coordinates=True``).

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to query, in any of the :ref:`supported forms <Introduction_Forms>`.
    element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'bond', 'system'}, default 'system'
        Element level at which attributes are retrieved.
    selection : int, tuple, list, numpy.ndarray or str, default 'all'
        Subset of elements (interpreted at the level set by `element`) to use when retrieving
        attributes. Either a 0-based index collection or a selection string parsed according to
        :ref:`Introduction_Selection`.
    structure_indices : int, tuple, list, numpy.ndarray or 'all', default 'all'
        0-based indices of structures to include in the query. Required for structural attributes (e.g., coordinates, box, time).
    mask : str or array-like, optional
        Additional subset applied after selection. It can be a selection string,
        a collection of 0-based element indices, or a Boolean array with one
        entry per element.
    syntax : str, default 'MolSysMT'
        Selection syntax used when `selection` is a string. See :ref:`Introduction_Selection`.
    get_missing_bonds : bool, default True
        Whether to infer and return bond information on the fly when bond-related attributes
        are requested and the input form lacks explicit connectivity. The inference uses the
        form backend’s heuristics (distance/chemistry-aware thresholds).
    output_type : {'values', 'dictionary'}, default 'values'
        Output format:
        - ``value` — **convenience mode**:
          * if exactly **one** attribute is requested, return its value directly;
          * if **multiple** attributes are requested, return a **list** of values following
            the order in which the attributes were provided in `**kwargs`.
        - ``'dictionary'`` — return a dictionary mapping attribute names to values.
    chemical_state : {'reference', 'structure'} or int, default 'reference'
        Chemical state used to resolve state-dependent atom, component, and bond
        attributes. A non-negative integer selects a state by its 0-based index.
        ``'structure'`` resolves the unique state associated with the requested
        structures of a native MolSys. State identifiers are not accepted
        because they need not be unique.
    skip_digestion : bool, default False
        Whether to skip MolSysMT’s internal argument digestion mechanism.

        MolSysMT includes a built-in digestion system that validates and normalizes
        function arguments. This process checks types, shapes, and values, and automatically
        adjusts them when possible to meet expected formats.

        Setting `skip_digestion=True` disables this process, which may improve performance
        in workflows where inputs are already validated. Use with caution: only set this to
        `True` if you are certain all input arguments are correct and consistent
    **kwargs
        Attribute flags selecting which values to retrieve (e.g., ``n_atoms=True``,
        ``coordinates=True``, ``time=True``, ``box=True``, etc.). Only attributes flagged
        as `True` are returned.

    Returns
    -------
    Any or list or dict or None
        Depending on `output_type`:
        - If ``output_type == 'values'`` and a single attribute is requested: the attribute value. This value can be
        `None` if the attribute is not found in the system.
        - If ``output_type == 'values'`` and multiple attributes are requested: a list with values
          in the order given by `**kwargs`.
        - If ``output_type == 'dictionary'``: a dictionary ``{attribute_name: value}``.

    Raises
    ------
    NotSupportedFormError
        If the molecular system has an unsupported form.
    ArgumentError
        If any input argument is invalid or inconsistent, including malformed
        selections and out-of-range element, mask, or structure indices.
    NotWithThisFormError
        If a form declares a requested attribute but provides neither a
        compatible direct getter, registered derivation, nor usable attribute
        pipe.

    Notes
    -----
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.
    - A request may combine attributes from different element levels when an
      incompatible attribute has exactly one catalog-supported level. MolSysMT
      evaluates that attribute at its supported level and preserves the input
      attribute order. For example, with ``element='atom'``, ``coordinates``
      are evaluated on atoms while ``structure_id`` is evaluated on the system.
      The atom selection is not applied to system-level attributes.
    - Native Structures and MolSys objects expose stored temperature, potential
      energy, and kinetic energy series. Total energy is returned only when both
      energy components are present. OpenMM Context and Simulation objects expose
      temperature only when their integrator defines it.
    - Native Topology and MolSys objects resolve state-dependent atom chemistry,
      components, and bonds from ``chemical_state``. The default uses the
      reference-state rules. Access is rejected when multiple states exist
      without a reference and no explicit index is supplied.
    - ``isotope`` is stable atom metadata. Rich bond attributes keep integral
      and fractional order, relationship type, aromaticity, conjugation,
      stereochemistry and reference atoms, direction, component participation,
      and evidence independent.
    - State inventory attributes such as ``chemical_state_index`` and
      ``chemical_state_id`` continue to describe every state even when
      ``chemical_state`` selects one state for other requested attributes.
    - Explicit integer state selection currently requires a native Topology or
      MolSys. Convert an external form before querying a non-reference state.
    - ``chemical_state='structure'`` requires a native MolSys and rejects
      missing associations or structure selections spanning multiple states.
    - Form-independent attributes such as box lengths, angles, shape, and volume
      are derived from the box matrix when the source form exposes that matrix
      but does not implement a dedicated getter.

    See Also
    --------
    :func:`molsysmt.basic.select`
        Select elements from a molecular system.
    :func:`molsysmt.basic.get_attributes`
        Get the list of available attributes for a molecular system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> molsys = systems['T4 lysozyme L99A']['181l.h5msm']
    >>> msm.get(molsys, element='group', selection=[10,11,12], n_atoms=True)
    [9, 4, 8]
    >>> msm.get(molsys, element='molecule', selection='molecule_type=="water"', n_molecules=True)
    136
    >>> msm.get(molsys, element='bond', selection=[0,1,2,3,4], bonded_atoms=True)
    [0, 1, 2, 3, 4, 8]
    >>> from molsysmt.native import Topology
    >>> topology = Topology(n_atoms=3)
    >>> msm.set(topology, element='atom', formal_charge=[0, -1, 1])
    >>> msm.get(topology, element='atom', chemical_state=0, formal_charge=True)
    [0, -1, 1]
    >>> msm.set(topology, element='atom', isotope=[13, None, 2])
    >>> msm.get(topology, element='atom', isotope=True)[0]
    13
    >>> msm.get(topology, element='system', n_chemical_states=True,
    ...         reference_chemical_state_index=True)
    [1, 0]
    >>> import numpy as np
    >>> from molsysmt.native import MolSys
    >>> molsys = MolSys(n_atoms=1)
    >>> molsys.structures.coordinates = msm.pyunitwizard.quantity(np.zeros((2, 1, 3)), 'nm')
    >>> msm.get(molsys, structure_chemical_state_index=True)
    [0, 0]

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Get`.

    .. versionadded:: 1.0.0
    """

    from .. import select, where_is_attribute, get_form, convert
    from molsysmt.form import _dict_modules
    from molsysmt.attribute import attributes, bonds_are_required_to_get_attribute
    from molsysmt.attribute import is_topological_attribute, is_structural_attribute

    form = get_form(molecular_system)

    if isinstance(form, (list, tuple)):
        attributes_filter = _dict_modules[form[0]].attributes.copy()
        for aux_form in form[1:]:
            for aux_attribute, aux_bool in _dict_modules[aux_form].attributes.items():
                if aux_bool:
                    attributes_filter[aux_attribute]=True
    else:
        attributes_filter = _dict_modules[form].attributes

    in_attributes = []
    # print(f"DEBUG: get() called with kwargs keys: {list(kwargs.keys())}")
    for key in kwargs.keys():
        if kwargs[key]:
            in_attributes.append(key)
    # print(f"DEBUG: in_attributes resolved: {in_attributes}")

    if not isinstance(molecular_system, (list, tuple)):
        molecular_system = [molecular_system]
        form = [form]

    if not in_attributes:
        return {} if output_type == 'dictionary' else []

    if any(attributes[attribute]['runs_on_structures'] for attribute in in_attributes):
        from ._index_validation import validate_structure_indices

        structure_indices = validate_structure_indices(
            molecular_system, structure_indices, 'molsysmt.get'
        )

    attribute_groups = _group_attributes_by_element(element, selection, in_attributes)

    if attribute_groups and (len(attribute_groups) > 1 or element not in attribute_groups):
        output_dictionary = {}

        for target_element, target_attributes in attribute_groups.items():
            if element == 'system' and not is_all(selection):
                use_requested_selection = target_element == 'atom'
            else:
                use_requested_selection = target_element == element
            target_selection = selection if use_requested_selection else 'all'
            target_mask = mask if use_requested_selection else None
            output_dictionary.update(
                get(
                    molecular_system,
                    element=target_element,
                    selection=target_selection,
                    structure_indices=structure_indices,
                    chemical_state=chemical_state,
                    mask=target_mask,
                    syntax=syntax,
                    get_missing_bonds=get_missing_bonds,
                    output_type='dictionary',
                    skip_digestion=True,
                    **{attribute: True for attribute in target_attributes},
                )
            )

        if output_type == 'dictionary':
            return {attribute: output_dictionary[attribute] for attribute in in_attributes}

        output = [output_dictionary[attribute] for attribute in in_attributes]
        return output[0] if len(output) == 1 else output

    if not is_all(selection):
        indices = select(molecular_system, element=element, selection=selection,
                         chemical_state=chemical_state, mask=mask, syntax=syntax,
                         skip_digestion=True)
    else:
        if (mask is None) or (is_all(mask)):
            indices = 'all'
        else:
            indices = select(molecular_system, element=element, selection=mask,
                             chemical_state=chemical_state, syntax=syntax,
                             skip_digestion=True)

    piped_molecular_systems, piped_attributes = _piped_molecular_system(molecular_system, element, in_attributes)

    if piped_molecular_systems is None:

        output = []

        for in_attribute in in_attributes:

            if attributes_filter[in_attribute]:

                dict_indices = {}
                if element != 'system':
                    if attributes[in_attribute]['runs_on_elements']:
                        dict_indices['indices'] = indices
                if attributes[in_attribute]['runs_on_structures']:
                    dict_indices['structure_indices'] = structure_indices

                aux_item, aux_form = where_is_attribute(molecular_system, in_attribute, skip_digestion=True)

                if aux_item is None:
                    result = None
                else:
                    getter_name = f'get_{in_attribute}_from_{element}'
                    aux_get = getattr(_dict_modules[aux_form], getter_name, None)
                    if aux_get is None:
                        from molsysmt._private.attribute_derivation import (
                            NOT_DERIVABLE,
                            derive_attribute,
                        )

                        result = derive_attribute(
                            _dict_modules[aux_form],
                            aux_item,
                            in_attribute,
                            element,
                            structure_indices=dict_indices.get('structure_indices', 'all'),
                        )
                        if result is NOT_DERIVABLE:
                            from molsysmt._private.smonitor import NotWithThisFormError

                            raise NotWithThisFormError(
                                caller='molsysmt.get',
                                form=aux_form,
                                requested_attribute=in_attribute,
                                message=(
                                    f"Form {aux_form!r} declares attribute {in_attribute!r} but "
                                    f"does not implement {getter_name!r}, a registered derivation, "
                                    "or a usable attribute pipe."
                                ),
                            )
                    else:
                        result = aux_get(aux_item, **dict_indices)

                if (result is not None) and in_attribute.endswith('_id'):
                    result = _coerce_ids_to_string(result)
                if in_attribute == 'alternate_location' and result is not None:
                    result = _coerce_alternate_location_ids(result)

            else:

                result = None

            output.append(result)

    else:

        output_dictionary = {}

        for aux_molecular_system, aux_attributes in zip(piped_molecular_systems, piped_attributes):

            if aux_molecular_system is None:
                aux_molecular_system = molecular_system

            aux_dict = get(aux_molecular_system, element=element, selection=indices,
                           structure_indices=structure_indices, chemical_state=chemical_state,
                           mask=mask, syntax=syntax,
                           get_missing_bonds=get_missing_bonds, output_type='dictionary', skip_digestion=False,
                           **{ii:True for ii in aux_attributes})

            output_dictionary.update(aux_dict)

        output = []

        for in_attribute in in_attributes:

            output.append(output_dictionary[in_attribute])

    import pyunitwizard as puw

    _CANONICAL_UNITS = {
        'coordinates': 'nm',
        'box': 'nm',
        'box_lengths': 'nm',
        'box_angles': 'radians',
        'box_volume': 'nm**3',
        'velocities': 'nm/ps',
        'time': 'ps',
        'time_step': 'ps',
        'potential_energy': 'kJ/mol',
        'kinetic_energy': 'kJ/mol',
        'total_energy': 'kJ/mol',
        'temperature': 'K',
        'b_factor': 'nm**2',
    }

    def _standardize(value, attribute):
        if value is None:
            return None
        if puw.is_quantity(value):
            return puw.standardize(value)
        if attribute in _CANONICAL_UNITS:
            return puw.quantity(value, _CANONICAL_UNITS[attribute])
        return value

    if output_type=='values':
        if len(output) == 1:
            return _standardize(output[0], in_attributes[0])
        else:
            return [_standardize(val, attr) for val, attr in zip(output, in_attributes)]
    elif output_type=='dictionary':
        return {ii: _standardize(jj, ii) for ii, jj in zip(in_attributes, output)}
        
def _coerce_ids_to_string(value):
    """Normalize *_id values to Python/NumPy strings, preserving shape."""
    if is_iterable_of_iterables(value):
        return [_coerce_ids_to_string(aux_value) for aux_value in value]
    else:
        arr = np.asarray(value)
        if arr.shape == ():
            return str(arr.astype(str))
        else:
            return arr.astype(str).tolist()

def _coerce_alternate_location_ids(value):
    """Ensure alternate_location entries carry string atom_id keys/values."""
    output = []
    for structure_dict in value:
        if structure_dict is None:
            output.append(structure_dict)
            continue
        new_struct = {}
        for key, entry in structure_dict.items():
            new_entry = dict(entry)
            if 'atom_id' in new_entry:
                new_entry['atom_id'] = _coerce_ids_to_string(new_entry['atom_id'])
            new_struct[str(key)] = new_entry
        output.append(new_struct)
    return output


def _group_attributes_by_element(element, selection, in_attributes):
    """Group attributes by an unambiguous catalog-compatible element."""
    from molsysmt.attribute import attributes

    output = {}
    atom_selection_from_system = element == 'system' and not is_all(selection)

    for attribute in in_attributes:
        supported_elements = attributes[attribute]['get_from']
        target_element = element

        if atom_selection_from_system and 'atom' in supported_elements:
            target_element = 'atom'
        elif supported_elements and element not in supported_elements:
            if len(supported_elements) == 1:
                target_element = supported_elements[0]

        output.setdefault(target_element, []).append(attribute)

    return output

def _piped_molecular_system(molecular_system, element, in_attributes):
    """Resolve piped attributes across items for get(); returns tuple (item, attribute list) or (None, None)."""


    from .. import select, where_is_attribute, get_form, convert
    from molsysmt.form import _dict_modules
    from molsysmt.attribute import attributes, bonds_are_required_to_get_attribute
    from molsysmt.attribute import is_topological_attribute, is_structural_attribute

    topological_pipes = {}
    structural_pipes = {}
    any_pipes = {}

    form = get_form(molecular_system)

    if not isinstance(molecular_system, (list, tuple)):
        molecular_system = [molecular_system]
        form = [form]

    for aux_form in form:
        topological_pipes[aux_form] = getattr(_dict_modules[aux_form], f'piped_topological_attribute')
        structural_pipes[aux_form] = getattr(_dict_modules[aux_form], f'piped_structural_attribute')
        any_pipes[aux_form] = getattr(_dict_modules[aux_form], f'piped_any_attribute')

    not_piped = all([ii is None for ii in topological_pipes.values()]) & \
                all([ii is None for ii in structural_pipes.values()]) & \
                all([ii is None for ii in any_pipes.values()])  

    single_attribute_has_direct_getter = False
    if len(in_attributes) == 1:
        in_attribute = next(iter(in_attributes))
        _, aux_form = where_is_attribute(molecular_system, in_attribute, skip_digestion=True)
        if aux_form is not None:
            getter_name = f'get_{in_attribute}_from_{element}'
            single_attribute_has_direct_getter = (
                getattr(_dict_modules[aux_form], getter_name, None) is not None
            )
            if not single_attribute_has_direct_getter:
                from molsysmt._private.attribute_derivation import can_derive_attribute

                single_attribute_has_direct_getter = can_derive_attribute(
                    _dict_modules[aux_form],
                    in_attribute,
                    element,
                )

    if not_piped or single_attribute_has_direct_getter:

        return None, None

    else:

        aux_topological_attributes = []
        aux_topological_pipes = []
        aux_structural_attributes = []
        aux_structural_pipes = []
        aux_any_pipes = []

        bonds_required_by_attributes = False

        for in_attribute in in_attributes:
            bonds_required_by_attributes += bonds_are_required_to_get_attribute(in_attribute, element,
                                                                                skip_digestion=True)
            if is_topological_attribute(in_attribute, skip_digestion=True):
                aux_topological_attributes.append(in_attribute)
                _, aux_form = where_is_attribute(molecular_system, in_attribute, skip_digestion=True)
                if aux_form is not None:
                    if topological_pipes[aux_form] is not None:
                        if topological_pipes[aux_form] not in aux_topological_pipes:
                            aux_topological_pipes.append(topological_pipes[aux_form])
                    if any_pipes[aux_form] is not None:
                        if any_pipes[aux_form] not in aux_any_pipes:
                            aux_any_pipes.append(any_pipes[aux_form])
            elif is_structural_attribute(in_attribute, skip_digestion=True):
                _, aux_form = where_is_attribute(molecular_system, in_attribute)
                aux_structural_attributes.append(in_attribute)
                if aux_form is not None:
                    if structural_pipes[aux_form] is not None:
                        if structural_pipes[aux_form] not in aux_structural_pipes:
                            aux_structural_pipes.append(structural_pipes[aux_form])
                    if any_pipes[aux_form] is not None:
                        if any_pipes[aux_form] not in aux_any_pipes:
                            aux_any_pipes.append(any_pipes[aux_form])

        n_top_pipes = len(aux_topological_pipes)
        n_str_pipes = len(aux_structural_pipes)
        n_any_pipes = len(aux_any_pipes)

        n_top_atts = len(aux_topological_attributes)
        n_str_atts = len(aux_structural_attributes)

        output_systems = []
        output_attributes = []

        if n_top_pipes==0 and n_str_pipes==0 and n_any_pipes==0:

            output_systems = None
            output_attributes = None

        elif n_top_atts>0 and n_str_atts==0:

            if n_top_pipes==1:

                aux_molecular_system = convert(molecular_system, to_form=aux_topological_pipes[0],
                                               get_missing_bonds=bonds_required_by_attributes, skip_digestion=True)

            else:

                aux_molecular_system = convert(molecular_system, to_form='molsysmt.Topology',
                                               get_missing_bonds=bonds_required_by_attributes, skip_digestion=True)

            output_systems.append(aux_molecular_system)
            output_attributes.append(aux_topological_attributes)

        elif n_top_atts==0 and n_str_atts>0:

            if n_str_pipes == 1:

                aux_molecular_system = convert(molecular_system, to_form=aux_structural_pipes[0],
                                               skip_digestion=True)

            else:

                aux_molecular_system = convert(molecular_system, to_form='molsysmt.Structures', skip_digestion=True)

            output_systems.append(aux_molecular_system)
            output_attributes.append(aux_structural_attributes)

        else:

            if n_any_pipes == 1:

                aux_molecular_system = convert(molecular_system, to_form=aux_any_pipes[0],
                                               get_missing_bonds=bonds_required_by_attributes, skip_digestion=True)

                output_systems.append(aux_molecular_system)
                output_attributes.append(aux_topological_attributes+aux_structural_attributes)

            elif n_any_pipes > 1:

                aux_molecular_system = convert(molecular_system, to_form='molsysmt.MolSys',
                                               get_missing_bonds=bonds_required_by_attributes, skip_digestion=True)

                output_systems.append(aux_molecular_system)
                output_attributes.append(aux_topological_attributes+aux_structural_attributes)

            elif n_any_pipes == 0:

                if n_top_pipes == 1:

                    aux_molecular_system = convert(molecular_system, to_form=aux_topological_pipes[0],
                                                   get_missing_bonds=bonds_required_by_attributes, skip_digestion=True)

                elif n_top_pipes > 1:

                    aux_molecular_system = convert(molecular_system, to_form='molsysmt.Topology',
                                                   get_missing_bonds=bonds_required_by_attributes, skip_digestion=True)

                else:

                    aux_molecular_system = None

                output_systems.append(aux_molecular_system)
                output_attributes.append(aux_topological_attributes)

                if n_str_pipes == 1:

                    aux_molecular_system = convert(molecular_system, to_form=aux_structural_pipes[0],
                                                   skip_digestion=True)

                elif n_str_pipes > 1:

                    aux_molecular_system = convert(molecular_system, to_form='molsysmt.Structures', skip_digestion=True)

                else:

                    aux_molecular_system = None

                output_systems.append(aux_molecular_system)
                output_attributes.append(aux_structural_attributes)

    return output_systems, output_attributes
