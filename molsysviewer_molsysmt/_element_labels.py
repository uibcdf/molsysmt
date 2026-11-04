"""Explicit group-name predicates and canonical-code lookups; no molecular reader."""

from argdigest import arg_digest
from smonitor import signal

from ._element_common import _ElementUtilities, _utility_documentation
from ._element_templates import (
    _AminoAcidTemplates,
    _IonTemplates,
    _SaccharideTemplates,
    _TerminalCappingTemplates,
    _WaterTemplates,
)


def _label_documentation(name, module, *, local_skip=True):
    def decorate(function):
        function = _utility_documentation(name, module, local_skip=local_skip)(function)
        if name in {"get_1_letter_code_from_name", "get_standard_name"}:
            function.__doc__ += (
                "\nScientific qualification\n------------------------\n"
                "Canonical sequence-code recognition does not supply an atomic "
                "template or validate protonation. MolSysMT#549 tracks legacy "
                "variant-name mappings versus native protonation labels; no "
                "addon reinterpretation or chemical substitution is introduced.\n"
            )
        if name in {"is_n_terminal_capping", "is_c_terminal_capping"}:
            function.__doc__ += (
                "\nPeptide-end convention\n---------------------\n"
                "The predicate names the protected peptide end: ACE protects "
                "the N terminus; NME/NHE/NH2 protect the C terminus. Recognizing "
                "a cap name does not attach it or prepare the molecular system.\n"
            )
        return function

    return decorate


class _AminoAcidTools(_AminoAcidTemplates):
    _NAMES = (
        "get_bonded_atom_pairs",
        "get_expected_heavy_atoms",
        "get_expected_hydrogens",
        "get_group_db",
        "get_1_letter_code_from_name",
        "get_standard_name",
        "is_amino_acid",
    )

    @_label_documentation(
        "get_1_letter_code_from_name", "element.group.amino_acid", local_skip=True
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_1_letter_code_from_name(self, name, *, skip_digestion=False):
        return self._call_explicit(
            ("group", "amino_acid"), "get_1_letter_code_from_name", {"name": name}
        )

    @_label_documentation(
        "get_standard_name", "element.group.amino_acid", local_skip=True
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_standard_name(self, group_name, *, skip_digestion=False):
        return self._call_explicit(
            ("group", "amino_acid"), "get_standard_name", {"group_name": group_name}
        )

    @_label_documentation("is_amino_acid", "element.group.amino_acid", local_skip=True)
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_amino_acid(self, name, *, skip_digestion=False):
        return self._call_explicit(
            ("group", "amino_acid"), "is_amino_acid", {"name": name}
        )


class _IonTools(_IonTemplates):
    _NAMES = (
        "get_bonded_atom_pairs",
        "get_group_db",
        "is_ion",
    )

    @_label_documentation("is_ion", "element.group.ion", local_skip=True)
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_ion(self, name, *, skip_digestion=False):
        return self._call_explicit(("group", "ion"), "is_ion", {"name": name})


class _LipidTools(_ElementUtilities):
    _NAMES = ("is_lipid",)

    @_label_documentation("is_lipid", "element.group.lipid", local_skip=True)
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_lipid(self, name, *, skip_digestion=False):
        return self._call_explicit(("group", "lipid"), "is_lipid", {"name": name})


class _NucleotideTools(_ElementUtilities):
    _NAMES = ("is_nucleotide",)

    @_label_documentation("is_nucleotide", "element.group.nucleotide", local_skip=True)
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_nucleotide(self, name, *, skip_digestion=False):
        return self._call_explicit(
            ("group", "nucleotide"), "is_nucleotide", {"name": name}
        )


class _SaccharideTools(_SaccharideTemplates):
    _NAMES = (
        "get_bonded_atom_pairs",
        "get_group_db",
        "is_saccharide",
    )

    @_label_documentation("is_saccharide", "element.group.saccharide", local_skip=True)
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_saccharide(self, name, *, skip_digestion=False):
        return self._call_explicit(
            ("group", "saccharide"), "is_saccharide", {"name": name}
        )


class _TerminalCappingTools(_TerminalCappingTemplates):
    _NAMES = (
        "get_bonded_atom_pairs",
        "get_group_db",
        "is_c_terminal_capping",
        "is_n_terminal_capping",
        "is_terminal_capping",
    )

    @_label_documentation(
        "is_c_terminal_capping", "element.group.terminal_capping", local_skip=True
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_c_terminal_capping(self, name, *, skip_digestion=False):
        return self._call_explicit(
            ("group", "terminal_capping"), "is_c_terminal_capping", {"name": name}
        )

    @_label_documentation(
        "is_n_terminal_capping", "element.group.terminal_capping", local_skip=True
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_n_terminal_capping(self, name, *, skip_digestion=False):
        return self._call_explicit(
            ("group", "terminal_capping"), "is_n_terminal_capping", {"name": name}
        )

    @_label_documentation(
        "is_terminal_capping", "element.group.terminal_capping", local_skip=True
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_terminal_capping(self, name, *, skip_digestion=False):
        return self._call_explicit(
            ("group", "terminal_capping"), "is_terminal_capping", {"name": name}
        )


class _WaterTools(_WaterTemplates):
    _NAMES = (
        "get_bonded_atom_pairs",
        "is_water",
    )

    @_label_documentation("is_water", "element.group.water", local_skip=True)
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_water(self, name, *, skip_digestion=False):
        return self._call_explicit(("group", "water"), "is_water", {"name": name})
