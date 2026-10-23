"""Explicit read/calculation wrappers for the received topology operations."""

from argdigest import arg_digest
from smonitor import signal

from ._basic import _native_documentation


class _TopologyTools:
    _NAMES = (
        "get_bondgraph",
        "get_covalent_blocks",
        "get_covalent_paths",
        "get_dihedral_quartets",
    )

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    def _call(self, name, parameters, extra=None):
        from molsysmt import topology

        return self._owner._read(getattr(topology, name), parameters, extra)

    @_native_documentation("get_bondgraph", module="topology")
    @signal(tags=["addon", "topology"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_bondgraph(
        self,
        nodes_name="atom_index",
        selection="all",
        syntax="MolSysMT",
        to_form="networkx.Graph",
        *,
        chemical_state="reference",
        structure_indices="all",
        skip_digestion=False,
    ):
        return self._call(
            "get_bondgraph",
            {
                "nodes_name": nodes_name,
                "selection": selection,
                "syntax": syntax,
                "to_form": to_form,
                "chemical_state": chemical_state,
                "structure_indices": structure_indices,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_covalent_blocks", module="topology")
    @signal(tags=["addon", "topology"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_covalent_blocks(
        self,
        selection="all",
        remove_bonds=None,
        output_type="sets",
        syntax="MolSysMT",
        *,
        chemical_state="reference",
        structure_indices="all",
        skip_digestion=False,
    ):
        return self._call(
            "get_covalent_blocks",
            {
                "selection": selection,
                "remove_bonds": remove_bonds,
                "output_type": output_type,
                "syntax": syntax,
                "chemical_state": chemical_state,
                "structure_indices": structure_indices,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_covalent_paths", module="topology")
    @signal(tags=["addon", "topology"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_covalent_paths(
        self, path=None, selection="all", syntax="MolSysMT", *, skip_digestion=False
    ):
        return self._call(
            "get_covalent_paths",
            {"path": path, "selection": selection, "syntax": syntax},
        )

    @_native_documentation("get_dihedral_quartets", module="topology")
    @signal(tags=["addon", "topology"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_dihedral_quartets(
        self,
        with_blocks=False,
        selection="all",
        syntax="MolSysMT",
        *,
        skip_digestion=False,
        **kwargs,
    ):
        return self._call(
            "get_dihedral_quartets",
            {
                "with_blocks": with_blocks,
                "selection": selection,
                "syntax": syntax,
            },
            kwargs,
        )
