"""Explicit attribute metadata utilities, independent of the primary system."""

from argdigest import arg_digest
from smonitor import signal


class _AttributeTools:
    """Expose native metadata on an open view without a molecular reader."""

    _NAMES = (
        "get_argument_aliases",
        "is_attribute",
        "is_chemical_state_attribute",
        "is_structural_attribute",
        "is_topological_attribute",
        "is_mechanical_attribute",
        "bonds_are_required_to_get_attribute",
    )

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    @signal(tags=["addon", "metadata"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_argument_aliases(self, *, skip_digestion=False):
        """Returning the independent native argument-alias contract.

        Parameters
        ----------
        skip_digestion : bool, default=False
            Keyword-only addon validation control; the native utility has no
            digestion parameter and does not receive this argument.

        Returns
        -------
        dict
            Native versioned plain-data contract, including attribute synonyms
            and element-dependent aliases. Each call returns an independent copy.

        Notes
        -----
        Works with an open empty view. No molecular reader, synchronization,
        scene or history change is involved. Aliases describe native callable
        contracts; this utility does not apply them to other addon methods.

        Examples
        --------
        >>> import molsysviewer as msv
        >>> with msv.new_view() as view:
        ...     aliases = view.addons.molsysmt.attribute.get_argument_aliases()
        ...     print(aliases['element_attribute_aliases']['group']['name'])
        group_name
        """
        self._owner._view()
        from molsysmt.attribute import get_argument_aliases

        return get_argument_aliases()

    @signal(tags=["addon", "metadata"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_attribute(self, attribute, *, skip_digestion=False):
        """Checking native canonical attribute-name membership.

        Parameters
        ----------
        attribute : object
            Explicit name tested by the native membership predicate. Synonyms
            are not resolved; unsupported input types retain native errors.
        skip_digestion : bool, default=False
            Keyword-only addon validation control, not passed to this native
            utility because it has no digestion parameter.

        Returns
        -------
        bool
            Whether the explicit value is a registered canonical attribute name.

        Notes
        -----
        Works with an open empty view. No molecular reader, synchronization,
        scene or history change is involved. An unknown hashable name returns
        False, without claiming availability on any particular molecular system.

        Examples
        --------
        >>> import molsysviewer as msv
        >>> with msv.new_view() as view:
        ...     print(view.addons.molsysmt.attribute.is_attribute('atom_name'))
        ...     print(view.addons.molsysmt.attribute.is_attribute('atom_names'))
        True
        False
        """
        self._owner._view()
        from molsysmt.attribute import is_attribute

        return is_attribute(attribute)

    @signal(tags=["addon", "metadata"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_chemical_state_attribute(self, attribute, skip_digestion=False):
        """Checking native chemical-state attribute classification.

        Parameters
        ----------
        attribute : object
            Explicit attribute name; native validation and aliases are retained.
        skip_digestion : bool, default=False
            Forwarded unchanged to the native public validation boundary.

        Returns
        -------
        bool
            Whether native metadata marks the attribute as chemical-state data.

        Notes
        -----
        Works with an open empty view, without molecular reading, synchronization
        or scene/history changes. Classification does not resolve a chemical
        state or establish that a particular system supplies the attribute.
        """
        self._owner._view()
        from molsysmt.attribute import is_chemical_state_attribute

        return is_chemical_state_attribute(
            attribute=attribute, skip_digestion=skip_digestion
        )

    @signal(tags=["addon", "metadata"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_structural_attribute(self, attribute, skip_digestion=False):
        """Checking native structural attribute classification.

        Parameters
        ----------
        attribute : object
            Explicit attribute name; native validation and aliases are retained.
        skip_digestion : bool, default=False
            Forwarded unchanged to the native public validation boundary.

        Returns
        -------
        bool
            Whether native metadata marks the attribute as structural data.

        Notes
        -----
        Works with an open empty view, without molecular reading, synchronization
        or scene/history changes. Shared atom-inventory attributes can also be
        topological; these classification categories are not disjoint.
        """
        self._owner._view()
        from molsysmt.attribute import is_structural_attribute

        return is_structural_attribute(
            attribute=attribute, skip_digestion=skip_digestion
        )

    @signal(tags=["addon", "metadata"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_topological_attribute(self, attribute, skip_digestion=False):
        """Checking the native compatibility classification for topology.

        Parameters
        ----------
        attribute : object
            Explicit attribute name; native validation and aliases are retained.
        skip_digestion : bool, default=False
            Forwarded unchanged to the native public validation boundary.

        Returns
        -------
        bool
            Native classification, also True for nonstructural chemical-state
            attributes. It does not promise chemistry on a pure Topology.

        Notes
        -----
        Works with an open empty view, without molecular reading, synchronization
        or scene/history changes. This is metadata, not a domain-availability
        test; preserve its overlap with the other classification predicates.
        """
        self._owner._view()
        from molsysmt.attribute import is_topological_attribute

        return is_topological_attribute(
            attribute=attribute, skip_digestion=skip_digestion
        )

    @signal(tags=["addon", "metadata"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_mechanical_attribute(self, attribute, skip_digestion=False):
        """Checking native molecular-mechanics attribute classification.

        Parameters
        ----------
        attribute : object
            Explicit attribute name; native validation and aliases are retained.
        skip_digestion : bool, default=False
            Forwarded unchanged to the native public validation boundary.

        Returns
        -------
        bool
            Whether native metadata marks the attribute as mechanical data.

        Notes
        -----
        Works with an open empty view, without molecular reading, synchronization
        or scene/history changes. This neither loads an engine nor establishes
        parameterization, energy/force availability or scientific readiness.
        """
        self._owner._view()
        from molsysmt.attribute import is_mechanical_attribute

        return is_mechanical_attribute(
            attribute=attribute, skip_digestion=skip_digestion
        )

    @signal(tags=["addon", "metadata"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def bonds_are_required_to_get_attribute(
        self, attribute, from_element=None, skip_digestion=False
    ):
        """Checking native connectivity requirements for an attribute query.

        Parameters
        ----------
        attribute : str
            Explicit canonical attribute name, validated by MolSysMT.
        from_element : str or None, default=None
            Explicit source element. None checks the requested attribute alone;
            the current view's selection or system never supplies this value.
        skip_digestion : bool, default=False
            Forwarded unchanged to the native public validation boundary.

        Returns
        -------
        bool
            True for graph attributes or a bond/component source axis. Reading
            stored atom/group/chain/molecule/entity inventory needs no bonds.

        Notes
        -----
        Works with an open empty view, without molecular reading, synchronization
        or scene/history changes. This describes reading declared data, not
        preparation or conversion-specific inference of missing inventory.

        Examples
        --------
        >>> import molsysviewer as msv
        >>> with msv.new_view() as view:
        ...     tools = view.addons.molsysmt.attribute
        ...     print(tools.bonds_are_required_to_get_attribute('molecule_index', 'atom'))
        ...     print(tools.bonds_are_required_to_get_attribute('atom_index', 'component'))
        False
        True
        """
        self._owner._view()
        from molsysmt.attribute import bonds_are_required_to_get_attribute

        return bonds_are_required_to_get_attribute(
            attribute=attribute,
            from_element=from_element,
            skip_digestion=skip_digestion,
        )
