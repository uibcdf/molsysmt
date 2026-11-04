"""Native component/molecule readers and the explicit legacy group heuristic."""

from argdigest import arg_digest
from smonitor import signal

from ._basic import _native_documentation
from ._element_common import _call_explicit, _utility_documentation
from ._element_hierarchy import _HierarchyTools, _reader_documentation


def _domain_documentation(name, scope, *, local_skip=False):
    def decorate(function):
        function = _reader_documentation(name, scope, local_skip=local_skip)(function)
        if scope == "component":
            function.__doc__ += (
                "Component data require the native ChemicalStates domain. "
                "Reference-state and explicit reconstruction semantics remain "
                "native; the addon never chooses chemistry from the canvas frame "
                "or changes stable molecule membership.\n"
            )
        else:
            function.__doc__ += (
                "Stable molecule membership remains distinct from state-local "
                "components. Local redefine_* projections are returned without "
                "assignment; native chemistry prerequisites and unsupported "
                "combinations retain their errors.\n"
            )
        return function

    return decorate


def _legacy_documentation(function):
    function = _native_documentation(
        "small_molecule_is_amino_acid", module="element.group.small_molecule"
    )(function)
    function.__doc__ = function.__doc__.replace(
        "\nReturns\n-------",
        "\nskip_digestion : bool, default=False\n"
        "    Keyword-only addon validation control; not passed to the native helper.\n\nReturns\n-------",
        1,
    )
    function.__doc__ += (
        "\n\nView integration\n----------------\n"
        "Uses the current loaded system through the serialized molecular reader "
        "without assignment or scene reconciliation. This is the native legacy "
        "heuristic: a catalogued small-molecule group name and the presence of "
        "CA, CB, C, O and N atom names. It does not validate chemical connectivity "
        "or stereochemistry, prepare the system or create a stored classification. "
        "group_name remains explicit. Native errors and Boolean results are "
        "preserved. The local skip control is not forwarded; the native helper "
        "has no such flag. A loaded open owner is required.\n"
    )
    return function


class _ComponentTools(_HierarchyTools):
    _MODULE = "component"
    _NAMES = (
        "get_component_id",
        "get_component_index",
        "get_component_name",
        "get_component_type",
        "get_n_components",
        "is_component_type",
    )

    @_domain_documentation("get_component_id", "component")
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_component_id(
        self,
        element="component",
        selection="all",
        redefine_indices=False,
        redefine_ids=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_component_id",
            {
                "element": element,
                "selection": selection,
                "redefine_indices": redefine_indices,
                "redefine_ids": redefine_ids,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_domain_documentation("get_component_index", "component")
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_component_index(
        self,
        element="component",
        selection="all",
        redefine_indices=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_component_index",
            {
                "element": element,
                "selection": selection,
                "redefine_indices": redefine_indices,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_domain_documentation("get_component_name", "component")
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_component_name(
        self,
        element="component",
        selection="all",
        redefine_indices=False,
        redefine_names=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_component_name",
            {
                "element": element,
                "selection": selection,
                "redefine_indices": redefine_indices,
                "redefine_names": redefine_names,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_domain_documentation("get_component_type", "component")
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_component_type(
        self,
        element="component",
        selection="all",
        redefine_indices=False,
        redefine_types=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_component_type",
            {
                "element": element,
                "selection": selection,
                "redefine_indices": redefine_indices,
                "redefine_types": redefine_types,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_domain_documentation("get_n_components", "component")
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_n_components(
        self,
        selection="all",
        redefine_components=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_n_components",
            {
                "selection": selection,
                "redefine_components": redefine_components,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_utility_documentation("is_component_type", "element.component", local_skip=True)
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_component_type(self, component_type, *, skip_digestion=False):
        return _call_explicit(
            self._owner,
            ("component",),
            "is_component_type",
            {"component_type": component_type},
        )


class _MoleculeTools(_HierarchyTools):
    _MODULE = "molecule"
    _NAMES = (
        "get_molecule_id",
        "get_molecule_index",
        "get_molecule_name",
        "get_molecule_type",
        "get_n_molecules",
        "is_molecule_type",
    )

    @_domain_documentation("get_molecule_id", "molecule")
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_molecule_id(
        self,
        element="molecule",
        selection="all",
        redefine_indices=False,
        redefine_ids=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_molecule_id",
            {
                "element": element,
                "selection": selection,
                "redefine_indices": redefine_indices,
                "redefine_ids": redefine_ids,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_domain_documentation("get_molecule_index", "molecule")
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_molecule_index(
        self,
        element="molecule",
        selection="all",
        redefine_indices=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_molecule_index",
            {
                "element": element,
                "selection": selection,
                "redefine_indices": redefine_indices,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_domain_documentation("get_molecule_name", "molecule")
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_molecule_name(
        self,
        element="molecule",
        selection="all",
        redefine_indices=False,
        redefine_names=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_molecule_name",
            {
                "element": element,
                "selection": selection,
                "redefine_indices": redefine_indices,
                "redefine_names": redefine_names,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_domain_documentation("get_molecule_type", "molecule")
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_molecule_type(
        self,
        element="molecule",
        selection="all",
        redefine_indices=False,
        redefine_types=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_molecule_type",
            {
                "element": element,
                "selection": selection,
                "redefine_indices": redefine_indices,
                "redefine_types": redefine_types,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_domain_documentation("get_n_molecules", "molecule", local_skip=True)
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_n_molecules(
        self,
        selection="all",
        redefine_molecules=False,
        syntax="MolSysMT",
        *,
        skip_digestion=False,
    ):
        return self._call(
            "get_n_molecules",
            {
                "selection": selection,
                "redefine_molecules": redefine_molecules,
                "syntax": syntax,
            },
        )

    @_utility_documentation("is_molecule_type", "element.molecule", local_skip=True)
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_molecule_type(self, molecule_type, *, skip_digestion=False):
        return _call_explicit(
            self._owner,
            ("molecule",),
            "is_molecule_type",
            {"molecule_type": molecule_type},
        )


class _SmallMoleculeTools(_HierarchyTools):
    _NAMES = ("small_molecule_is_amino_acid", "is_small_molecule")

    @_legacy_documentation
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def small_molecule_is_amino_acid(self, group_name, *, skip_digestion=False):
        from molsysmt.element.group.small_molecule import small_molecule_is_amino_acid

        return self._owner._read(
            small_molecule_is_amino_acid, {"group_name": group_name}
        )

    @_utility_documentation(
        "is_small_molecule", "element.group.small_molecule", local_skip=True
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_small_molecule(self, name, *, skip_digestion=False):
        return _call_explicit(
            self._owner,
            ("group", "small_molecule"),
            "is_small_molecule",
            {"name": name},
        )
