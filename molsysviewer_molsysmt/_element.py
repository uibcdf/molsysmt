"""Element namespace with explicit utilities and current-system hierarchy readers."""

from argdigest import arg_digest
from smonitor import signal

from ._basic import _native_documentation
from ._element_domains import _ComponentTools, _MoleculeTools, _SmallMoleculeTools
from ._element_hierarchy import _ChainTools, _EntityTools, _reader_documentation


def _utility_documentation(name, module="element", *, local_skip=False):
    def decorate(function):
        function = _native_documentation(name, module=module, bind_primary=False)(
            function
        )
        function.__doc__ += (
            "\n\nView integration\n----------------\n"
            "Works with an open empty view. Scientific inputs stay explicit; "
            "no primary molecular reader, synchronization, scene/history change "
            "or assignment is involved. Native validation, warnings, return "
            "types and result ownership are retained.\n"
        )
        if local_skip:
            function.__doc__ = function.__doc__.replace(
                "\nReturns\n-------",
                "\nskip_digestion : bool, default=False\n"
                "    Keyword-only addon validation control, not forwarded to "
                "the native utility.\n\nReturns\n-------",
                1,
            )
            function.__doc__ += (
                "skip_digestion is a keyword-only addon validation control. "
                "This native utility has no such parameter; it receives no "
                "skip flag and retains its own validation.\n"
            )
        if name == "is_composed_of":
            function.__doc__ += (
                "This is the native declared relation between two element-level "
                "names, not a query of the actual contents of view.molsys.\n"
            )
        return function

    return decorate


class _ElementUtilities:
    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    def _call_explicit(self, module, name, parameters):
        self._owner._view()
        import molsysmt

        namespace = molsysmt.element
        for part in module:
            namespace = getattr(namespace, part)
        return getattr(namespace, name)(**parameters)


class _AtomTools(_ElementUtilities):
    _NAMES = (
        "is_atom_type",
        "normalize_atom_types",
        "get_atom_type_from_atom_name",
        "get_atom_type_from_atom_ff_type",
    )

    @_utility_documentation("is_atom_type", "element.atom")
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_atom_type(self, atom_type, skip_digestion=False):
        return self._call_explicit(
            ("atom",),
            "is_atom_type",
            {"atom_type": atom_type, "skip_digestion": skip_digestion},
        )

    @_utility_documentation("normalize_atom_types", "element.atom")
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def normalize_atom_types(self, atom_type, isotope=None, skip_digestion=False):
        return self._call_explicit(
            ("atom",),
            "normalize_atom_types",
            {
                "atom_type": atom_type,
                "isotope": isotope,
                "skip_digestion": skip_digestion,
            },
        )

    @_utility_documentation(
        "get_atom_type_from_atom_name", "element.atom", local_skip=True
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_atom_type_from_atom_name(self, atom_name, *, skip_digestion=False):
        return self._call_explicit(
            ("atom",), "get_atom_type_from_atom_name", {"atom_name": atom_name}
        )

    @_utility_documentation("get_atom_type_from_atom_ff_type", "element.atom")
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_atom_type_from_atom_ff_type(
        self, atom_ff_type, typing_scheme="autodock4", skip_digestion=False
    ):
        return self._call_explicit(
            ("atom",),
            "get_atom_type_from_atom_ff_type",
            {
                "atom_ff_type": atom_ff_type,
                "typing_scheme": typing_scheme,
                "skip_digestion": skip_digestion,
            },
        )


class _GroupTools(_ElementUtilities):
    _NAMES = (
        "is_group_type",
        "get_group_type_from_group_name",
        "get_group_type",
        "small_molecule",
    )

    def __init__(self, owner):
        super().__init__(owner)
        self.small_molecule = _SmallMoleculeTools(owner)

    @_reader_documentation("get_group_type", "group")
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_group_type(
        self,
        element="group",
        selection="all",
        redefine_types=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        from molsysmt.element.group import get_group_type

        return self._owner._read(
            get_group_type,
            {
                "element": element,
                "selection": selection,
                "redefine_types": redefine_types,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_utility_documentation("is_group_type", "element.group", local_skip=True)
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_group_type(self, group_type, *, skip_digestion=False):
        return self._call_explicit(
            ("group",), "is_group_type", {"group_type": group_type}
        )

    @_utility_documentation("get_group_type_from_group_name", "element.group")
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_group_type_from_group_name(self, group_name, skip_digestion=False):
        return self._call_explicit(
            ("group",),
            "get_group_type_from_group_name",
            {"group_name": group_name, "skip_digestion": skip_digestion},
        )


class _ElementTools(_ElementUtilities):
    _NAMES = (
        "atom",
        "group",
        "chain",
        "entity",
        "component",
        "molecule",
        "is_element",
        "is_composed_of",
    )

    def __init__(self, owner):
        super().__init__(owner)
        self.atom = _AtomTools(owner)
        self.group = _GroupTools(owner)
        self.chain = _ChainTools(owner)
        self.entity = _EntityTools(owner)
        self.component = _ComponentTools(owner)
        self.molecule = _MoleculeTools(owner)

    @_utility_documentation("is_element", local_skip=True)
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_element(self, element, *, skip_digestion=False):
        return self._call_explicit((), "is_element", {"element": element})

    @_utility_documentation("is_composed_of", local_skip=True)
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_composed_of(self, element_1, element_2, *, skip_digestion=False):
        return self._call_explicit(
            (), "is_composed_of", {"element_1": element_1, "element_2": element_2}
        )
