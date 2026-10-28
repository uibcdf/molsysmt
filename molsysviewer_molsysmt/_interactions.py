"""Explicit interaction recognition; native results remain separate from the scene."""

from argdigest import arg_digest
from smonitor import signal

from ._basic import _native_documentation


class _InteractionsTools:
    def __init__(self, owner):
        self.hbonds = _HbondTools(owner)

    def __dir__(self):
        return ["hbonds"]


class _HbondTools:
    _NAMES = (
        "get_donor_atoms",
        "get_acceptor_atoms",
        "get_hbond_sites",
        "get_hbond_site_directions",
    )

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    def _call(self, name, parameters):
        from molsysmt.interactions import hbonds

        return self._owner._read(getattr(hbonds, name), parameters)

    @_native_documentation("get_donor_atoms", module="interactions.hbonds")
    @signal(tags=["addon", "interactions", "hbonds"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_donor_atoms(
        self,
        selection="all",
        inclusion_rules=None,
        exclusion_rules=None,
        default_inclusion_rules=True,
        default_exclusion_rules=True,
        syntax="MolSysMT",
        *,
        skip_digestion=False,
    ):
        return self._call(
            "get_donor_atoms",
            {
                "selection": selection,
                "inclusion_rules": inclusion_rules,
                "exclusion_rules": exclusion_rules,
                "default_inclusion_rules": default_inclusion_rules,
                "default_exclusion_rules": default_exclusion_rules,
                "syntax": syntax,
            },
        )

    @_native_documentation("get_acceptor_atoms", module="interactions.hbonds")
    @signal(tags=["addon", "interactions", "hbonds"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_acceptor_atoms(
        self,
        selection="all",
        inclusion_rules=None,
        exclusion_rules=None,
        default_inclusion_rules=True,
        default_exclusion_rules=True,
        syntax="MolSysMT",
        *,
        skip_digestion=False,
    ):
        return self._call(
            "get_acceptor_atoms",
            {
                "selection": selection,
                "inclusion_rules": inclusion_rules,
                "exclusion_rules": exclusion_rules,
                "default_inclusion_rules": default_inclusion_rules,
                "default_exclusion_rules": default_exclusion_rules,
                "syntax": syntax,
            },
        )

    @_native_documentation("get_hbond_sites", module="interactions.hbonds")
    @signal(tags=["addon", "interactions", "hbonds"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_hbond_sites(
        self,
        selection="all",
        structure_indices="all",
        chemical_state="reference",
        method="elemental_nitrogen_oxygen",
        assume_complete_connectivity=False,
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        max_matches=100000,
    ):
        return self._call(
            "get_hbond_sites",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "method": method,
                "assume_complete_connectivity": assume_complete_connectivity,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
                "max_matches": max_matches,
            },
        )

    @_native_documentation("get_hbond_site_directions", module="interactions.hbonds")
    @signal(tags=["addon", "interactions", "hbonds"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_hbond_site_directions(
        self,
        selection="all",
        structure_indices="all",
        chemical_state="reference",
        method="ideal_local_geometry",
        site_method="smarts_donor_acceptor",
        assume_complete_connectivity=False,
        pbc=True,
        syntax="MolSysMT",
        heavy_mode="auto",
        skip_digestion=False,
        *,
        max_matches=100000,
    ):
        return self._call(
            "get_hbond_site_directions",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "method": method,
                "site_method": site_method,
                "assume_complete_connectivity": assume_complete_connectivity,
                "pbc": pbc,
                "syntax": syntax,
                "heavy_mode": heavy_mode,
                "skip_digestion": skip_digestion,
                "max_matches": max_matches,
            },
        )
