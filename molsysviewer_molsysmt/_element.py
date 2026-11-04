"""Element namespace with explicit utilities and current-system hierarchy readers."""

from argdigest import arg_digest
from smonitor import signal

from ._element_common import _ElementUtilities, _utility_documentation
from ._element_domains import _ComponentTools, _MoleculeTools, _SmallMoleculeTools
from ._element_hierarchy import _ChainTools, _EntityTools, _reader_documentation
from ._element_labels import (
    _AminoAcidTools,
    _IonTools,
    _LipidTools,
    _NucleotideTools,
    _SaccharideTools,
    _TerminalCappingTools,
    _WaterTools,
)
from ._element_templates import _GroupTemplates


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


class _GroupTools(_GroupTemplates):
    _NAMES = (
        "get_bonded_atom_pairs",
        "is_group_type",
        "get_group_type_from_group_name",
        "get_group_type",
        "small_molecule",
        "amino_acid",
        "ion",
        "lipid",
        "nucleotide",
        "saccharide",
        "terminal_capping",
        "water",
    )

    def __init__(self, owner):
        super().__init__(owner)
        self.small_molecule = _SmallMoleculeTools(owner)
        self.amino_acid = _AminoAcidTools(owner)
        self.ion = _IonTools(owner)
        self.lipid = _LipidTools(owner)
        self.nucleotide = _NucleotideTools(owner)
        self.saccharide = _SaccharideTools(owner)
        self.terminal_capping = _TerminalCappingTools(owner)
        self.water = _WaterTools(owner)

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
