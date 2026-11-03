"""Shared public query methods and direct providers for native domains."""

import numpy as np
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.chemical_state import resolve_chemical_state
from molsysmt._private.variables import is_all

_DIGEST = {
    "digestion_source": "molsysmt._private.argdigest.native_queries",
    "digestion_style": "registry",
    "function_source": "molsysmt._private.argdigest.native_queries",
    "normalization_source": "molsysmt._private.argdigest.native_queries",
}


class NativeQueries:
    """Providing the common public query experience to resident native domains."""

    @signal(tags=["native", "get"])
    @arg_digest(**_DIGEST)
    @resolve_chemical_state
    def get(
        self,
        element="system",
        selection="all",
        structure_indices="all",
        mask=None,
        syntax="MolSysMT",
        get_missing_bonds=True,
        output_type="values",
        skip_digestion=False,
        *,
        chemical_state="reference",
        **kwargs,
    ):
        """Getting attributes directly from this native object's domains.

        Parameters
        ----------
        element : str, default='system'
            Element level to query, such as atom, group or system.
        selection : str, int, list, tuple or numpy.ndarray, default='all'
            Elements to query, as positional indices or a selection expression.
        structure_indices : str, int, list, tuple or numpy.ndarray, default='all'
            Structure indices (0-based), preserving order and repetitions.
        mask : str, list, tuple, numpy.ndarray or None, default=None
            Additional selection intersected at the requested element level.
        syntax : str, default='MolSysMT'
            Syntax used to evaluate selection expressions.
        get_missing_bonds : bool, default=True
            Whether to obtain missing connectivity when required by the query.
        output_type : str, default='values'
            Return values, or an attribute dictionary with 'dictionary'.
        skip_digestion : bool, default=False
            Whether to skip digestion of arguments already satisfying the contract.
        chemical_state : str, int or None, default='reference'
            State used for state-dependent attributes, under basic.get rules.
            This argument is keyword-only to preserve existing MolSys calls.
        **kwargs
            Attribute flags, such as n_atoms=True or coordinates=True. Attribute
            aliases and value validation follow molsysmt.basic.get.

        Returns
        -------
        object
            One value, an ordered list of values, or an attribute dictionary.
            Quantities follow the session unit policy. Missing attributes retain
            the basic.get None behavior.

        Raises
        ------
        ArgumentError
            If a query option, attribute flag or selected index is invalid.
        UnknownArgumentError
            If a keyword is outside the public attribute catalogue.

        Notes
        -----
        Explicit index queries use known native providers without universal
        form discovery. Selection expressions and nested selections retain the
        existing general selector. This operation does not build or convert a
        molecular system. The specialized Structures getters remain available.
        ChemicalStates supplies stored atom/bond/component axes, counts,
        nullable atom assignments, bond fields, component labels and selected-state
        completeness directly. Formal charges are integers in elementary-charge
        units. Missing atom columns return None; missing bond fields retain one
        nullable entry per edge (two for stereo references). Its state inventory remains
        collection-wide. Unknown connectivity is not inferred by these queries.
        ChemicalStatesDict reads the corresponding typed columns directly;
        it does not decode a native collection or certify unrelated payload/history.

        See Also
        --------
        molsysmt.basic.get : Querying any supported molecular-system form.

        Examples
        --------
        >>> from molsysmt.native import Topology
        >>> topology = Topology(n_atoms=3)
        >>> topology.get(element='atom', selection=[2, 0], index=True)
        [2, 0]
        >>> topology.get(n_atoms=True, output_type='dictionary')
        {'n_atoms': 3}
        >>> from molsysmt.native import ChemicalStates
        >>> states = ChemicalStates(n_atoms=2)
        >>> states.append_state()
        0
        >>> states.get(n_bonds=True, connectivity_completeness=True)
        [0, 'unavailable']
        >>> states.add_bonds([[0, 1]])
        >>> states.get(element='bond', bond_order=True)
        [None]
        >>> states.get(formal_charge=True) is None
        True

        .. admonition:: User guide

           See :ref:`Tutorial_Get` for selections and result representations.

        .. versionadded:: 1.0.0
        """
        from molsysmt.basic.get import _get

        return _get(
            self,
            element=element,
            selection=selection,
            structure_indices=structure_indices,
            mask=mask,
            syntax=syntax,
            get_missing_bonds=get_missing_bonds,
            output_type=output_type,
            chemical_state=chemical_state,
            skip_digestion=True,
            _native=_NativeProvider(self),
            **kwargs,
        )

    @signal(tags=["native", "get"])
    @arg_digest(**_DIGEST)
    def info(
        self,
        element="system",
        selection="all",
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        mask=None,
        structure_indices="all",
        output_type="styler",
    ):
        """Summarizing this native object through the shared info table contract.

        Parameters
        ----------
        element : str, default='system'
            Element level to summarize, such as atom, group or system.
        selection : str, int, list, tuple or numpy.ndarray, default='all'
            Elements to include, as indices or a selection expression.
        syntax : str, default='MolSysMT'
            Syntax used to evaluate selection expressions.
        skip_digestion : bool, default=False
            Whether to skip digestion of already validated arguments.
        mask : str, list, tuple, numpy.ndarray or None, default=None
            Scope intersected with selection; system summaries select atoms.
        structure_indices : str, int, list, tuple or numpy.ndarray, default='all'
            Structure indices (0-based) to include in the summary.
        output_type : str, default='styler'
            Result representation: 'styler', 'dataframe' or 'dictionary'.

        Returns
        -------
        pandas.io.formats.style.Styler, pandas.DataFrame or list of dict
            The same summary columns and representations as basic.info.

        Raises
        ------
        ArgumentError
            If arguments or selected indices violate the public info contract.

        Notes
        -----
        Existing MolSys positional syntax and skip arguments retain their
        positions. Structure indices, output type and mask are keyword-only.
        Partial domains remain absent; a summary does not invent topology.

        See Also
        --------
        molsysmt.basic.info : Summarizing any supported molecular-system form.

        Examples
        --------
        >>> from molsysmt.native import Topology
        >>> topology = Topology(n_atoms=2)
        >>> topology.info(element='atoms', selection=1,
        ...               output_type='dataframe')['index'].tolist()
        [1]

        .. admonition:: User guide

           See :ref:`Tutorial_Info` for summary tables.

        .. versionadded:: 1.0.0
        """
        from molsysmt.basic.info import _info

        return _info(
            self,
            element=element,
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
            output_type=output_type,
            skip_digestion=True,
            mask=mask,
            _native=_NativeProvider(self),
        )


class _NativeProvider:
    """Resolve a single known resident domain without general form discovery."""

    def __init__(self, item):
        from molsysmt.form import _dict_modules
        from molsysmt.interactions.result import Interactions
        from molsysmt.native import (
            ChemicalStates,
            ChemicalStatesDict,
            MolSys,
            MolSysBuilder,
            Structures,
            Topology,
        )

        for cls in (
            MolSys,
            Topology,
            Structures,
            ChemicalStates,
            ChemicalStatesDict,
            MolSysBuilder,
            Interactions,
        ):
            if isinstance(item, cls):
                self.item = item
                self.form = "molsysmt." + cls.__name__
                self.module = _dict_modules[self.form]
                break
        else:
            raise TypeError(
                "Native queries require a supported resident native domain."
            )

    def form_of(self, item):
        return [self.form] if isinstance(item, (list, tuple)) else self.form

    def locate(self, item, attribute, include_none=False, skip_digestion=False):
        available = self.module.has_attribute(
            self.item,
            attribute,
            include_none=include_none,
            skip_digestion=True,
        )
        if not available and not include_none:
            available = self.module.has_attribute(
                self.item,
                attribute,
                include_none=True,
                skip_digestion=True,
            )
        return (self.item, self.form) if available else (None, None)

    def count(self, element):
        from molsysmt._private.smonitor import NotWithThisFormError
        from molsysmt.element import _singular_element_to_plural

        plural = _singular_element_to_plural.get(element)
        if element == "structure":
            plural = "structures"
        if plural is None:
            return None
        attribute = "n_" + plural
        if not self.module.attributes.get(attribute, False):
            return None
        getter = getattr(self.module, f"get_{attribute}_from_system", None)
        if getter is None:
            return None
        try:
            value = getter(self.item, skip_digestion=True)
        except NotWithThisFormError:
            return None
        return None if value is None else int(value)

    def get(self, item, **kwargs):
        from molsysmt.basic.get import _get

        return _get(self.item, _native=self, **kwargs)

    def select(
        self,
        item,
        selection="all",
        element="atom",
        mask=None,
        structure_indices="all",
        syntax="MolSysMT",
        chemical_state="reference",
        skip_digestion=False,
        **kwargs,
    ):
        from molsysmt.basic._index_validation import (
            normalize_mask,
            validate_element_indices,
        )

        # The public selector owns expression languages and nested selections.
        # Numeric native axes avoid its discovery and complementary-form search.
        expression = isinstance(selection, str) and not is_all(selection)
        simple = (
            selection is None
            or is_all(selection)
            or (
                isinstance(selection, (list, tuple, np.ndarray))
                and all(isinstance(index, (int, np.integer)) for index in selection)
            )
        )
        if expression or not simple or isinstance(mask, str) and not is_all(mask):
            from molsysmt.basic import select

            return select(
                self.item,
                selection=selection,
                element=element,
                mask=mask,
                structure_indices=structure_indices,
                syntax=syntax,
                chemical_state=chemical_state,
                skip_digestion=True,
                **kwargs,
            )
        if is_all(selection):
            indices = list(range(self.count(element)))
        else:
            indices = validate_element_indices(
                self.item,
                selection,
                element,
                "selection",
                "native.get",
                count_getter=self.count,
            )
        if indices is not None and mask is not None and not is_all(mask):
            normalized = normalize_mask(
                self.item,
                mask,
                element,
                "native.get",
                count_getter=self.count,
            )
            indices = np.intersect1d(indices, normalized).tolist()
        return indices
