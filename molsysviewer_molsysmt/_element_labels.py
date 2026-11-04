"""Explicit group-name predicates and canonical-code lookups; no molecular reader."""

from argdigest import arg_digest
from smonitor import signal

from ._element_common import _ElementUtilities, _utility_documentation


def _label_documentation(name, module, *, local_skip=True):
    def decorate(function):
        function = _utility_documentation(name, module, local_skip=local_skip)(function)
        if name == "get_1_letter_code_from_name":
            function.__doc__ += (
                "\nScientific qualification\n------------------------\n"
                "The inspected native source has an unreachable XLE/J mapping "
                "tracked in MolSysMT#545. The native result/error is preserved "
                "without an addon conversion or fallback; native qualification "
                "and receipt of its correction remain separate.\n"
            )
        if name in {"is_n_terminal_capping", "is_c_terminal_capping"}:
            function.__doc__ += (
                "\nScientific qualification\n------------------------\n"
                "MolSysMT#547 tracks a contradiction between the inspected native "
                "tables and documented N/C peptide-end meaning. This wrapper "
                "retains native Boolean membership without swapping it. These "
                "source checks do not qualify end-specific preparation; resolve "
                "the native contract before relying on that interpretation.\n"
            )
        return function

    return decorate


class _AminoAcidTools(_ElementUtilities):
    _NAMES = ("get_1_letter_code_from_name", "get_standard_name", "is_amino_acid")

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


class _IonTools(_ElementUtilities):
    _NAMES = ("is_ion",)

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


class _SaccharideTools(_ElementUtilities):
    _NAMES = ("is_saccharide",)

    @_label_documentation("is_saccharide", "element.group.saccharide", local_skip=True)
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_saccharide(self, name, *, skip_digestion=False):
        return self._call_explicit(
            ("group", "saccharide"), "is_saccharide", {"name": name}
        )


class _TerminalCappingTools(_ElementUtilities):
    _NAMES = ("is_c_terminal_capping", "is_n_terminal_capping", "is_terminal_capping")

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


class _WaterTools(_ElementUtilities):
    _NAMES = ("is_water",)

    @_label_documentation("is_water", "element.group.water", local_skip=True)
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_water(self, name, *, skip_digestion=False):
        return self._call_explicit(("group", "water"), "is_water", {"name": name})
