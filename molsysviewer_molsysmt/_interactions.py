"""Explicit native interaction tools; scientific results stay separate from the scene."""

from argdigest import arg_digest
from smonitor import signal

from ._basic import _native_documentation


class _InteractionsTools:
    def __init__(self, owner):
        self.hbonds = _HbondTools(owner)
        self.disulfides = _DisulfideTools(owner)
        self.ionic = _IonicTools(owner)
        self.hydrophobic = _HydrophobicTools(owner)
        self.halogen_bonds = _HalogenTools(owner)
        self.metal_coordination = _MetalCoordinationTools(owner)
        self.pi_pi = _PiPiTools(owner)
        self.cation_pi = _CationPiTools(owner)
        self.water_bridges = _WaterBridgeTools(owner)

    def __dir__(self):
        return [
            "hbonds",
            "disulfides",
            "ionic",
            "hydrophobic",
            "halogen_bonds",
            "metal_coordination",
            "pi_pi",
            "cation_pi",
            "water_bridges",
        ]


class _HbondTools:
    _NAMES = (
        "get_donor_atoms",
        "get_acceptor_atoms",
        "get_hbond_sites",
        "get_hbond_site_directions",
        "get_buch_hbonds",
        "get_luzard_chandler_hbonds",
        "get_hbonds",
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

    @_native_documentation("get_buch_hbonds", module="interactions.hbonds")
    @signal(tags=["addon", "interactions", "hbonds"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_buch_hbonds(
        self,
        selection="all",
        acceptors=None,
        donors=None,
        structure_indices="all",
        molecular_system_2=None,
        selection_2=None,
        acceptors_2=None,
        donors_2=None,
        structure_indices_2=None,
        distance_threshold="2.3 angstroms",
        pbc=True,
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        output_type="tuple",
    ):
        return self._call(
            "get_buch_hbonds",
            {
                "selection": selection,
                "acceptors": acceptors,
                "donors": donors,
                "structure_indices": structure_indices,
                "molecular_system_2": molecular_system_2,
                "selection_2": selection_2,
                "acceptors_2": acceptors_2,
                "donors_2": donors_2,
                "structure_indices_2": structure_indices_2,
                "distance_threshold": distance_threshold,
                "pbc": pbc,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
                "output_type": output_type,
            },
        )

    @_native_documentation("get_luzard_chandler_hbonds", module="interactions.hbonds")
    @signal(tags=["addon", "interactions", "hbonds"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_luzard_chandler_hbonds(
        self,
        selection="all",
        acceptors=None,
        donors=None,
        structure_indices="all",
        molecular_system_2=None,
        selection_2=None,
        acceptors_2=None,
        donors_2=None,
        structure_indices_2=None,
        distance_threshold="3.5 angstroms",
        angle_threshold="30 degrees",
        pbc=True,
        syntax="MolSysMT",
        *,
        output_type="tuple",
        skip_digestion=False,
    ):
        return self._call(
            "get_luzard_chandler_hbonds",
            {
                "selection": selection,
                "acceptors": acceptors,
                "donors": donors,
                "structure_indices": structure_indices,
                "molecular_system_2": molecular_system_2,
                "selection_2": selection_2,
                "acceptors_2": acceptors_2,
                "donors_2": donors_2,
                "structure_indices_2": structure_indices_2,
                "distance_threshold": distance_threshold,
                "angle_threshold": angle_threshold,
                "pbc": pbc,
                "syntax": syntax,
                "output_type": output_type,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_hbonds", module="interactions.hbonds")
    @signal(tags=["addon", "interactions", "hbonds"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_hbonds(
        self,
        selection="all",
        selection_2=None,
        structure_indices="all",
        chemical_state="reference",
        method="baker_hubbard",
        distance_threshold=None,
        angle_threshold=None,
        selection_mode="internal",
        pbc=True,
        assume_complete_connectivity=False,
        output_type="molsysmt.Interactions",
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        donor_hydrogen_pairs=None,
        acceptor_atom_indices=None,
        max_matches=100000,
        heavy_mode="auto",
        profile=None,
    ):
        return self._call(
            "get_hbonds",
            {
                "selection": selection,
                "selection_2": selection_2,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "method": method,
                "distance_threshold": distance_threshold,
                "angle_threshold": angle_threshold,
                "selection_mode": selection_mode,
                "pbc": pbc,
                "assume_complete_connectivity": assume_complete_connectivity,
                "output_type": output_type,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
                "donor_hydrogen_pairs": donor_hydrogen_pairs,
                "acceptor_atom_indices": acceptor_atom_indices,
                "max_matches": max_matches,
                "heavy_mode": heavy_mode,
                "profile": profile,
            },
        )


class _DisulfideTools:
    _NAMES = ("get_disulfide_candidates",)

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    def _call(self, name, parameters):
        from molsysmt.interactions import disulfides

        return self._owner._read(getattr(disulfides, name), parameters)

    @_native_documentation("get_disulfide_candidates", module="interactions.disulfides")
    @signal(tags=["addon", "interactions", "disulfides"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_disulfide_candidates(
        self,
        selection="all",
        structure_indices="all",
        max_bond_length=None,
        group_names=None,
        pbc=True,
        syntax="MolSysMT",
        sorted=True,
        skip_digestion=False,
        *,
        output_type="tuple",
    ):
        return self._call(
            "get_disulfide_candidates",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "max_bond_length": max_bond_length,
                "group_names": group_names,
                "pbc": pbc,
                "syntax": syntax,
                "sorted": sorted,
                "skip_digestion": skip_digestion,
                "output_type": output_type,
            },
        )


class _IonicTools:
    _NAMES = ("get_ionic_interactions",)

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    @_native_documentation("get_ionic_interactions", module="interactions.ionic")
    @signal(tags=["addon", "interactions", "ionic"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_ionic_interactions(
        self,
        distance_threshold,
        selection="all",
        selection_2=None,
        structure_indices="all",
        chemical_state="reference",
        method="minimum_distance",
        selection_mode="internal",
        pbc=True,
        assume_complete_connectivity=False,
        output_type="molsysmt.Interactions",
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        heavy_mode="auto",
    ):
        from molsysmt.interactions.ionic import get_ionic_interactions

        return self._owner._read(
            get_ionic_interactions,
            {
                "distance_threshold": distance_threshold,
                "selection": selection,
                "selection_2": selection_2,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "method": method,
                "selection_mode": selection_mode,
                "pbc": pbc,
                "assume_complete_connectivity": assume_complete_connectivity,
                "output_type": output_type,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
                "heavy_mode": heavy_mode,
            },
        )


class _HydrophobicTools:
    _NAMES = ("get_hydrophobic_interactions",)

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    @_native_documentation(
        "get_hydrophobic_interactions", module="interactions.hydrophobic"
    )
    @signal(tags=["addon", "interactions", "hydrophobic"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_hydrophobic_interactions(
        self,
        selection="all",
        selection_2=None,
        structure_indices="all",
        chemical_state="reference",
        method="atom_pair_distance",
        distance_threshold=None,
        selection_mode="internal",
        pbc=True,
        assume_complete_connectivity=False,
        output_type="molsysmt.Interactions",
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        max_matches=100000,
        heavy_mode="auto",
        profile=None,
    ):
        from molsysmt.interactions.hydrophobic import get_hydrophobic_interactions

        return self._owner._read(
            get_hydrophobic_interactions,
            {
                "selection": selection,
                "selection_2": selection_2,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "method": method,
                "distance_threshold": distance_threshold,
                "selection_mode": selection_mode,
                "pbc": pbc,
                "assume_complete_connectivity": assume_complete_connectivity,
                "output_type": output_type,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
                "max_matches": max_matches,
                "heavy_mode": heavy_mode,
                "profile": profile,
            },
        )


class _HalogenTools:
    _NAMES = ("get_halogen_bonds",)

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    @_native_documentation("get_halogen_bonds", module="interactions.halogen_bonds")
    @signal(tags=["addon", "interactions", "halogen_bonds"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_halogen_bonds(
        self,
        selection="all",
        selection_2=None,
        structure_indices="all",
        chemical_state="reference",
        method="distance_two_angles",
        distance_threshold=None,
        donor_angle_range=None,
        acceptor_angle_range=None,
        selection_mode="internal",
        pbc=True,
        assume_complete_connectivity=False,
        output_type="molsysmt.Interactions",
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        max_matches=100000,
        heavy_mode="auto",
        profile=None,
    ):
        from molsysmt.interactions.halogen_bonds import get_halogen_bonds

        return self._owner._read(
            get_halogen_bonds,
            {
                "selection": selection,
                "selection_2": selection_2,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "method": method,
                "distance_threshold": distance_threshold,
                "donor_angle_range": donor_angle_range,
                "acceptor_angle_range": acceptor_angle_range,
                "selection_mode": selection_mode,
                "pbc": pbc,
                "assume_complete_connectivity": assume_complete_connectivity,
                "output_type": output_type,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
                "max_matches": max_matches,
                "heavy_mode": heavy_mode,
                "profile": profile,
            },
        )


class _MetalCoordinationTools:
    _NAMES = ("get_metal_coordination",)

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    @_native_documentation(
        "get_metal_coordination", module="interactions.metal_coordination"
    )
    @signal(tags=["addon", "interactions", "metal_coordination"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_metal_coordination(
        self,
        selection="all",
        selection_2=None,
        structure_indices="all",
        chemical_state="reference",
        method="metal_ligand_distance",
        distance_threshold=None,
        selection_mode="internal",
        pbc=True,
        assume_complete_connectivity=False,
        output_type="molsysmt.Interactions",
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        max_matches=100000,
        heavy_mode="auto",
        profile=None,
    ):
        from molsysmt.interactions.metal_coordination import get_metal_coordination

        return self._owner._read(
            get_metal_coordination,
            {
                "selection": selection,
                "selection_2": selection_2,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "method": method,
                "distance_threshold": distance_threshold,
                "selection_mode": selection_mode,
                "pbc": pbc,
                "assume_complete_connectivity": assume_complete_connectivity,
                "output_type": output_type,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
                "max_matches": max_matches,
                "heavy_mode": heavy_mode,
                "profile": profile,
            },
        )


class _PiPiTools:
    _NAMES = ("get_pi_pi_interactions",)

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    @_native_documentation("get_pi_pi_interactions", module="interactions.pi_pi")
    @signal(tags=["addon", "interactions", "pi_pi"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_pi_pi_interactions(
        self,
        distance_threshold=None,
        angle_threshold=None,
        offset_threshold=None,
        planarity_threshold=None,
        selection="all",
        selection_2=None,
        structure_indices="all",
        chemical_state="reference",
        method="centroid_angle_offset",
        selection_mode="internal",
        pbc=True,
        assume_complete_connectivity=False,
        output_type="molsysmt.Interactions",
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        geometry="both",
        max_cyclic_block_size=256,
        max_matches=100000,
        heavy_mode="auto",
        profile=None,
    ):
        from molsysmt.interactions.pi_pi import get_pi_pi_interactions

        return self._owner._read(
            get_pi_pi_interactions,
            {
                "distance_threshold": distance_threshold,
                "angle_threshold": angle_threshold,
                "offset_threshold": offset_threshold,
                "planarity_threshold": planarity_threshold,
                "selection": selection,
                "selection_2": selection_2,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "method": method,
                "selection_mode": selection_mode,
                "pbc": pbc,
                "assume_complete_connectivity": assume_complete_connectivity,
                "output_type": output_type,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
                "geometry": geometry,
                "max_cyclic_block_size": max_cyclic_block_size,
                "max_matches": max_matches,
                "heavy_mode": heavy_mode,
                "profile": profile,
            },
        )


class _CationPiTools:
    _NAMES = ("get_cation_pi_interactions",)

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    @_native_documentation(
        "get_cation_pi_interactions", module="interactions.cation_pi"
    )
    @signal(tags=["addon", "interactions", "cation_pi"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_cation_pi_interactions(
        self,
        distance_threshold=None,
        angle_threshold=None,
        offset_threshold=None,
        planarity_threshold=None,
        selection="all",
        selection_2=None,
        structure_indices="all",
        chemical_state="reference",
        method="centroid_distance_angle",
        selection_mode="internal",
        pbc=True,
        assume_complete_connectivity=False,
        output_type="molsysmt.Interactions",
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        max_cyclic_block_size=256,
        max_matches=100000,
        heavy_mode="auto",
        profile=None,
    ):
        from molsysmt.interactions.cation_pi import get_cation_pi_interactions

        return self._owner._read(
            get_cation_pi_interactions,
            {
                "distance_threshold": distance_threshold,
                "angle_threshold": angle_threshold,
                "offset_threshold": offset_threshold,
                "planarity_threshold": planarity_threshold,
                "selection": selection,
                "selection_2": selection_2,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "method": method,
                "selection_mode": selection_mode,
                "pbc": pbc,
                "assume_complete_connectivity": assume_complete_connectivity,
                "output_type": output_type,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
                "max_cyclic_block_size": max_cyclic_block_size,
                "max_matches": max_matches,
                "heavy_mode": heavy_mode,
                "profile": profile,
            },
        )


class _WaterBridgeTools:
    _NAMES = ("get_water_bridges",)

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    @_native_documentation("get_water_bridges", module="interactions.water_bridges")
    @signal(tags=["addon", "interactions", "water_bridges"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_water_bridges(
        self,
        selection="all",
        selection_2=None,
        structure_indices="all",
        chemical_state="reference",
        method="hbond_water_path",
        distance_threshold=None,
        angle_threshold=None,
        selection_mode="internal",
        pbc=True,
        assume_complete_connectivity=False,
        output_type="molsysmt.Interactions",
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        hbond_method="baker_hubbard",
        hbond_profile=None,
        max_matches=100000,
        heavy_mode="auto",
        profile=None,
        order=1,
    ):
        from molsysmt.interactions.water_bridges import get_water_bridges

        return self._owner._read(
            get_water_bridges,
            {
                "selection": selection,
                "selection_2": selection_2,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "method": method,
                "distance_threshold": distance_threshold,
                "angle_threshold": angle_threshold,
                "selection_mode": selection_mode,
                "pbc": pbc,
                "assume_complete_connectivity": assume_complete_connectivity,
                "output_type": output_type,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
                "hbond_method": hbond_method,
                "hbond_profile": hbond_profile,
                "max_matches": max_matches,
                "heavy_mode": heavy_mode,
                "profile": profile,
                "order": order,
            },
        )
