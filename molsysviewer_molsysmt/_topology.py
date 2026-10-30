"""Explicit read/calculation wrappers for independent native domains."""

from argdigest import arg_digest
from smonitor import signal

from ._basic import _native_documentation


class _TopologyTools:
    _NAMES = ("get_sequence_alignment", "get_sequence_identity")

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    def _call(self, name, parameters, extra=None):
        from molsysmt import topology

        return self._owner._read(getattr(topology, name), parameters, extra)

    @_native_documentation("get_sequence_alignment", module="topology")
    @signal(tags=["addon", "topology"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_sequence_alignment(
        self,
        selection="all",
        reference_molecular_system=None,
        reference_selection="all",
        engine="Biopython",
        syntax="MolSysMT",
        prettyprint=False,
        alignment_index=0,
        skip_digestion=False,
    ):
        return self._call(
            "get_sequence_alignment",
            {
                "selection": selection,
                "reference_molecular_system": reference_molecular_system,
                "reference_selection": reference_selection,
                "engine": engine,
                "syntax": syntax,
                "prettyprint": prettyprint,
                "alignment_index": alignment_index,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_sequence_identity", module="topology")
    @signal(tags=["addon", "topology"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_sequence_identity(
        self,
        selection="all",
        reference_molecular_system=None,
        reference_selection="all",
        syntax="MolSysMT",
        engine="Biopython",
        *,
        skip_digestion=False,
    ):
        return self._call(
            "get_sequence_identity",
            {
                "selection": selection,
                "reference_molecular_system": reference_molecular_system,
                "reference_selection": reference_selection,
                "syntax": syntax,
                "engine": engine,
                "skip_digestion": skip_digestion,
            },
        )
