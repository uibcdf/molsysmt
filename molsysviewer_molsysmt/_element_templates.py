"""Explicit reference-template queries, independent of the current molecular system."""

from argdigest import arg_digest
from smonitor import signal

from ._element_common import _ElementUtilities, _utility_documentation


def _template_documentation(name, module, *, local_skip=False):
    def decorate(function):
        function = _utility_documentation(name, module, local_skip=local_skip)(function)
        function.__doc__ += (
            "\nReference templates\n-------------------\n"
            "All labels, atom names, indices and chemical context are explicit. "
            "This queries native reference data, not the connectivity or chemical "
            "state of view.molsys. No atoms/bonds are added, assigned or inferred "
            "in the view. Native unknown/template fallback, return containers "
            "and data layouts are preserved without addon caching.\n"
        )
        if name == "get_bonded_atom_pairs":
            function.__doc__ += (
                "Returned pairs use the supplied atom indices, or the native "
                "local positions when omitted; they are not resolved against "
                "the current molecular system. Missing templates and unsupported "
                "families retain native None/empty/error behavior.\n"
            )
        if name == "get_expected_hydrogens":
            function.__doc__ += (
                "pH and terminal/disulfide context remain caller choices. Native "
                "fixed reference rules are not environment-dependent pKa "
                "prediction and do not protonate the molecular system.\n"
            )
        if module.endswith("terminal_capping"):
            function.__doc__ += (
                "Cap classification uses the protected peptide end: ACE is "
                "N-terminal and NME/NHE/NH2 are C-terminal. Explicit reference "
                "lookup does not choose or attach a cap to the view.\n"
            )
        return function

    return decorate


class _GroupTemplates(_ElementUtilities):
    @_template_documentation("get_bonded_atom_pairs", "element.group", local_skip=True)
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_bonded_atom_pairs(
        self,
        group_name,
        atom_names,
        atom_indices=None,
        sorted=True,
        *,
        skip_digestion=False,
    ):
        return self._call_explicit(
            ("group",),
            "get_bonded_atom_pairs",
            {
                "group_name": group_name,
                "atom_names": atom_names,
                "atom_indices": atom_indices,
                "sorted": sorted,
            },
        )


class _AminoAcidTemplates(_ElementUtilities):
    @_template_documentation(
        "get_bonded_atom_pairs", "element.group.amino_acid", local_skip=False
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_bonded_atom_pairs(
        self,
        group_name,
        atom_names,
        atom_indices=None,
        sorted=True,
        skip_digestion=False,
    ):
        return self._call_explicit(
            ("group", "amino_acid"),
            "get_bonded_atom_pairs",
            {
                "group_name": group_name,
                "atom_names": atom_names,
                "atom_indices": atom_indices,
                "sorted": sorted,
                "skip_digestion": skip_digestion,
            },
        )

    @_template_documentation(
        "get_expected_heavy_atoms", "element.group.amino_acid", local_skip=True
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_expected_heavy_atoms(
        self, group_name, present_atom_names=None, *, skip_digestion=False
    ):
        return self._call_explicit(
            ("group", "amino_acid"),
            "get_expected_heavy_atoms",
            {"group_name": group_name, "present_atom_names": present_atom_names},
        )

    @_template_documentation(
        "get_expected_hydrogens", "element.group.amino_acid", local_skip=True
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_expected_hydrogens(
        self,
        group_name,
        present_atom_names=None,
        pH=7.4,
        is_n_terminal=False,
        is_c_terminal=False,
        is_disulfide=False,
        *,
        skip_digestion=False,
    ):
        return self._call_explicit(
            ("group", "amino_acid"),
            "get_expected_hydrogens",
            {
                "group_name": group_name,
                "present_atom_names": present_atom_names,
                "pH": pH,
                "is_n_terminal": is_n_terminal,
                "is_c_terminal": is_c_terminal,
                "is_disulfide": is_disulfide,
            },
        )

    @_template_documentation(
        "get_group_db", "element.group.amino_acid", local_skip=True
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_group_db(self, group_name, *, skip_digestion=False):
        return self._call_explicit(
            ("group", "amino_acid"), "get_group_db", {"group_name": group_name}
        )


class _IonTemplates(_ElementUtilities):
    @_template_documentation(
        "get_bonded_atom_pairs", "element.group.ion", local_skip=False
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_bonded_atom_pairs(
        self,
        group_name,
        atom_names,
        atom_indices=None,
        sorted=True,
        skip_digestion=False,
    ):
        return self._call_explicit(
            ("group", "ion"),
            "get_bonded_atom_pairs",
            {
                "group_name": group_name,
                "atom_names": atom_names,
                "atom_indices": atom_indices,
                "sorted": sorted,
                "skip_digestion": skip_digestion,
            },
        )

    @_template_documentation("get_group_db", "element.group.ion", local_skip=True)
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_group_db(self, group_name, *, skip_digestion=False):
        return self._call_explicit(
            ("group", "ion"), "get_group_db", {"group_name": group_name}
        )


class _SaccharideTemplates(_ElementUtilities):
    @_template_documentation(
        "get_bonded_atom_pairs", "element.group.saccharide", local_skip=True
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_bonded_atom_pairs(
        self,
        group_name,
        atom_names,
        atom_indices=None,
        sorted=True,
        *,
        skip_digestion=False,
    ):
        return self._call_explicit(
            ("group", "saccharide"),
            "get_bonded_atom_pairs",
            {
                "group_name": group_name,
                "atom_names": atom_names,
                "atom_indices": atom_indices,
                "sorted": sorted,
            },
        )

    @_template_documentation(
        "get_group_db", "element.group.saccharide", local_skip=True
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_group_db(self, group_name, *, skip_digestion=False):
        return self._call_explicit(
            ("group", "saccharide"), "get_group_db", {"group_name": group_name}
        )


class _SmallMoleculeTemplates(_ElementUtilities):
    @_template_documentation(
        "get_bonded_atom_pairs", "element.group.small_molecule", local_skip=True
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_bonded_atom_pairs(
        self,
        group_name,
        atom_names,
        atom_indices=None,
        sorted=True,
        *,
        skip_digestion=False,
    ):
        return self._call_explicit(
            ("group", "small_molecule"),
            "get_bonded_atom_pairs",
            {
                "group_name": group_name,
                "atom_names": atom_names,
                "atom_indices": atom_indices,
                "sorted": sorted,
            },
        )

    @_template_documentation(
        "get_group_db", "element.group.small_molecule", local_skip=True
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_group_db(self, group_name, *, skip_digestion=False):
        return self._call_explicit(
            ("group", "small_molecule"), "get_group_db", {"group_name": group_name}
        )


class _TerminalCappingTemplates(_ElementUtilities):
    @_template_documentation(
        "get_bonded_atom_pairs", "element.group.terminal_capping", local_skip=True
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_bonded_atom_pairs(
        self,
        group_name,
        atom_names,
        atom_indices=None,
        sorted=True,
        *,
        skip_digestion=False,
    ):
        return self._call_explicit(
            ("group", "terminal_capping"),
            "get_bonded_atom_pairs",
            {
                "group_name": group_name,
                "atom_names": atom_names,
                "atom_indices": atom_indices,
                "sorted": sorted,
            },
        )

    @_template_documentation(
        "get_group_db", "element.group.terminal_capping", local_skip=True
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_group_db(self, group_name, *, skip_digestion=False):
        return self._call_explicit(
            ("group", "terminal_capping"), "get_group_db", {"group_name": group_name}
        )


class _WaterTemplates(_ElementUtilities):
    @_template_documentation(
        "get_bonded_atom_pairs", "element.group.water", local_skip=True
    )
    @signal(tags=["addon", "element"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_bonded_atom_pairs(
        self, atom_names, atom_indices=None, sorted=True, *, skip_digestion=False
    ):
        return self._call_explicit(
            ("group", "water"),
            "get_bonded_atom_pairs",
            {"atom_names": atom_names, "atom_indices": atom_indices, "sorted": sorted},
        )
