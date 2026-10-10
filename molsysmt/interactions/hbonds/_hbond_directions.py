"""Bounded fixed-state direction planning and sparse block geometry."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.execution.reducer import Reducer
from molsysmt._private.execution.sparse_accumulator import SparseColumnAccumulator
from molsysmt._private.smonitor import (
    MemoryBudgetExceededError,
    StructuralInconsistencyError,
)

PATTERNS = (
    "[O;X1;+0]=[C;X3;+0;!$(C(=O)[O,S,P])]",
    "[n;+0;X2;H0]",
    "[N;+0;X1]#[C;+0;X2]",
)
MODELS = {
    0: "unsupported",
    1: "observed_donor_hydrogen",
    2: "carbonyl_trigonal",
    3: "aromatic_nitrogen_bisector",
    4: "nitrile_linear",
}
TOLERANCE = 1e-12
CALLER = "molsysmt.interactions.hbonds.get_hbond_site_directions"


def build_site_plan(source, sites, assume_complete, max_matches):
    """Classify recognized anchors without truncating their supporting graph."""
    from molsysmt.basic import get
    from molsysmt.topology import get_substructure_matches
    from molsysmt.topology._chemical_graph import chemical_graph_context

    source, _, state, _, _, bonds, _ = chemical_graph_context(
        source, sites["chemical_state_index"], "all", assume_complete, CALLER
    )
    matches = get_substructure_matches(
        source,
        PATTERNS,
        chemical_state=sites["chemical_state_index"],
        assume_complete_connectivity=assume_complete,
        max_matches=max_matches,
    )
    symbols = np.asarray(get(source, element="atom", atom_type=True))
    adjacency = {}
    for first, second in bonds:
        adjacency.setdefault(int(first), []).append(int(second))
        adjacency.setdefault(int(second), []).append(int(first))
    dative = (
        state.bonds.loc[state.bonds["bond_type"] == "dative"]
        if len(state.bonds)
        else state.bonds
    )
    coordinated = set(dative[["atom1_index", "atom2_index"]].to_numpy().ravel())
    environments = {}
    for oxygen, carbon in matches["matches"][0]:
        neighbors = sorted(adjacency.get(int(carbon), ()))
        candidates = [
            atom for atom in neighbors if atom != oxygen and symbols[atom] != "H"
        ]
        candidates = candidates or [atom for atom in neighbors if atom != oxygen]
        environments[int(oxygen)] = (2, [int(oxygen), int(carbon), *candidates[:1]])
    for (nitrogen,) in matches["matches"][1]:
        neighbors = sorted(adjacency.get(int(nitrogen), ()))
        if len(neighbors) == 2:
            environments[int(nitrogen)] = (3, [int(nitrogen), *neighbors])
    for nitrogen, carbon in matches["matches"][2]:
        environments[int(nitrogen)] = (4, [int(nitrogen), int(carbon)])
    entries = [(1, list(pair), 0) for pair in sites["donor_hydrogen_pairs"]]
    for atom in sites["acceptor_atom_indices"]:
        model, support = environments.get(int(atom), (0, [int(atom)]))
        if atom in coordinated:
            model, support = 0, [int(atom)]
        entries.append((model, support, 1))
    atoms, offsets, edges, edge_indices, models, roles, anchors = (
        [],
        [0],
        [],
        [],
        [],
        [],
        [],
    )
    slots, slot_indices = [], []
    for site, (model, support, role) in enumerate(entries):
        atoms.extend(support)
        offsets.append(len(atoms))
        models.append(model)
        roles.append(role)
        anchors.append(support[0])
        local_edges = []
        if model:
            local_edges.append((support[0], support[1]))
            if model in (2, 3) and len(support) == 3:
                local_edges.append(
                    (support[1] if model == 2 else support[0], support[2])
                )
            slots.extend([site] * (2 if model == 2 else 1))
            slot_indices.extend(range(2 if model == 2 else 1))
        edge_indices.append(local_edges)
        edges.extend(local_edges)
    edges = np.unique(np.asarray(edges, dtype=np.int64).reshape(-1, 2), axis=0)
    edge_lookup = {tuple(edge): index for index, edge in enumerate(edges)}
    site_edges = np.full((len(entries), 2), -1, dtype=np.int64)
    for site, local_edges in enumerate(edge_indices):
        for position, edge in enumerate(local_edges):
            site_edges[site, position] = edge_lookup[edge]
    return dict(
        site_atom_indices=np.asarray(anchors, dtype=np.int64),
        site_roles=np.asarray(roles, dtype=np.uint8),
        site_models=np.asarray(models, dtype=np.uint8),
        support_atom_indices=np.asarray(atoms, dtype=np.int64),
        support_atom_offsets=np.asarray(offsets, dtype=np.int64),
        edges=edges,
        site_edges=site_edges,
        universe=np.unique(atoms).astype(np.int64),
        slot_sites=np.asarray(slots, dtype=np.int64),
        slot_indices=np.asarray(slot_indices, dtype=np.uint8),
        geometry_software=matches["software"],
    )


def normalize(values):
    """Return normalized dimensionless vectors, leaving degeneracy undefined."""
    norm = np.linalg.norm(values, axis=-1, keepdims=True)
    return np.divide(
        values, norm, out=np.full_like(values, np.nan), where=norm > TOLERANCE
    )


class DirectionReducer(Reducer):
    """Pack finite directions and actual support images in structure/site order."""

    def __init__(self, plan, sites, frames, periodic, budget):
        self.plan, self.frames, self.periodic, self.budget = (
            plan,
            frames,
            periodic,
            budget,
        )
        self.local_edges = np.searchsorted(plan["universe"], plan["edges"])
        self.offset = 0
        static_bytes = sum(
            value.nbytes for value in plan.values() if isinstance(value, np.ndarray)
        )
        static_bytes += sum(
            value.nbytes for value in sites.values() if isinstance(value, np.ndarray)
        )
        status_bytes = len(frames) * len(plan["site_models"])
        self.fixed = static_bytes * 4 + status_bytes * 2 + budget // 4
        self._check(0)
        self.status = np.broadcast_to(
            np.where(plan["site_models"] == 0, 0, 2).astype(np.uint8),
            (len(frames), len(plan["site_models"])),
        ).copy()
        self.metadata = dict(
            schema="molsysmt.hbond_site_directions@1",
            sites=sites,
            donor_hydrogen_pairs=sites["donor_hydrogen_pairs"],
            acceptor_atom_indices=sites["acceptor_atom_indices"],
            **{
                key: plan[key]
                for key in (
                    "site_atom_indices",
                    "site_roles",
                    "site_models",
                    "support_atom_indices",
                    "support_atom_offsets",
                )
            },
            evaluated_structure_indices=frames,
            atom_source_indices=sites["atom_source_indices"],
            selected_atom_indices=sites["selected_atom_indices"],
            chemical_state_index=sites["chemical_state_index"],
            site_method=sites["method"],
            assume_complete_connectivity=sites["assume_complete_connectivity"],
            scope="selected_anchors_with_full_source_support",
            method="ideal_local_geometry",
            evidence="declared_chemistry_and_observed_bond_vectors",
            software={**sites["software"], **plan["geometry_software"]},
            codes=dict(
                site_roles={0: "donor", 1: "acceptor"},
                site_models=MODELS.copy(),
                status={0: "unsupported", 1: "defined", 2: "undefined"},
            ),
            parameters=dict(
                pbc=periodic,
                pbc_policy="mic_when_box_available",
                degeneracy_tolerance=TOLERANCE,
                patterns=PATTERNS,
                image_convention="r_support + image @ row_box; anchor image is zero",
                carbonyl_reference="lowest-index heavy covalent substituent; otherwise indexed H",
            ),
            method_reference=dict(
                software="RDKit",
                commit="cbfb37abddcd5b5feeac97d53530ae6be83cac0d",
                documentation="https://www.rdkit.org/docs/source/rdkit.Chem.Features.FeatDirUtilsRD.html",
                role="geometric_inspiration_only_not_exact_implementation_parity",
                attribution_role="geometric_inspiration",
            ),
            execution=dict(execution="no_geometry", numeric_ram_budget=budget),
            units=dict(directions="dimensionless", origins="configured_length"),
        )
        schema = dict(
            directions=(np.float64, (3,)),
            origins=(np.float64, (3,)),
            direction_site_indices=(np.int64, ()),
            direction_structure_indices=(np.int64, ()),
            direction_structure_positions=(np.int64, ()),
            direction_indices=(np.uint8, ()),
            image_counts=(np.int64, ()),
        )
        self.rows = SparseColumnAccumulator(
            schema, budget_bytes=budget, fixed_bytes=self.fixed
        )
        self.images = SparseColumnAccumulator(
            {"image_vectors": (np.int32, (3,))},
            budget_bytes=budget,
            fixed_bytes=self.fixed,
        )

    def _check(self, sparse_bytes):
        predicted = self.fixed + sparse_bytes * 6
        if predicted > self.budget:
            raise MemoryBudgetExceededError(
                reason="Estimated site-direction status, packing and block work exceed the RAM budget.",
                predicted_bytes=predicted,
                available_bytes=self.budget,
                caller=CALLER,
            )

    def initialize(self, metadata):
        self.offset = 0

    def consume(self, chunk):
        from molsysmt.pbc._whole_participants import validate_periodic_boxes
        from molsysmt.structure._vectors import evaluate_endpoint_vectors

        plan = self.plan
        coordinates = chunk["coordinates"]
        n_structures = len(coordinates)
        box = chunk.get("box") if self.periodic else None
        if box is not None:
            validate_periodic_boxes(box, n_structures, caller=CALLER)
        _, _, edge_directions, edge_images = evaluate_endpoint_vectors(
            coordinates[:, self.local_edges[:, 0]],
            coordinates[:, self.local_edges[:, 1]],
            box,
            True,
            True,
            caller=CALLER,
        )
        n_slots, n_sites = len(plan["slot_sites"]), len(plan["site_models"])
        directions = np.full((n_structures, n_slots, 3), np.nan)
        support_images = np.zeros((n_structures, n_sites, 3, 3), dtype=np.int64)
        for model in (1, 2, 3, 4):
            which_slots = np.flatnonzero(
                plan["site_models"][plan["slot_sites"]] == model
            )
            if not len(which_slots):
                continue
            which_sites = plan["slot_sites"][which_slots]
            first = plan["site_edges"][which_sites, 0]
            u = edge_directions[:, first]
            support_images[:, which_sites, 1] = edge_images[:, first]
            if model in (1, 4):
                directions[:, which_slots] = u if model == 1 else -u
                continue
            second = plan["site_edges"][which_sites, 1]
            usable = second >= 0
            v = edge_directions[:, np.maximum(second, 0)].copy()
            v[:, ~usable] = np.nan
            if model == 3:
                directions[:, which_slots] = -normalize(u + v)
                degenerate = np.linalg.norm(np.cross(u, v), axis=-1) <= TOLERANCE
                directions[:, which_slots] = np.where(
                    degenerate[..., None], np.nan, directions[:, which_slots]
                )
                support_images[:, which_sites, 2] = edge_images[
                    :, np.maximum(second, 0)
                ]
            else:
                transverse = normalize(v - np.sum(v * u, axis=-1, keepdims=True) * u)
                signs = np.where(plan["slot_indices"][which_slots] == 0, 1.0, -1.0)
                directions[:, which_slots] = (
                    -0.5 * u + (np.sqrt(3.0) / 2.0) * transverse * signs[None, :, None]
                )
                support_images[:, which_sites, 2] = (
                    edge_images[:, first].astype(np.int64)
                    + edge_images[:, np.maximum(second, 0)]
                )
        finite = np.isfinite(directions).all(axis=-1)
        positions, slots = np.nonzero(finite)
        sites = plan["slot_sites"][slots]
        counts = np.diff(plan["support_atom_offsets"])[sites]
        image_mask = np.arange(3)[None, :] < counts[:, None]
        packed_images = support_images[positions, sites][image_mask]
        limits = np.iinfo(np.int32)
        if np.any((packed_images < limits.min) | (packed_images > limits.max)):
            raise StructuralInconsistencyError(
                reason="Composed support images exceed int32 storage.", caller=CALLER
            )
        columns = dict(
            directions=directions[positions, slots],
            origins=coordinates[
                positions,
                np.searchsorted(plan["universe"], plan["site_atom_indices"][sites]),
            ],
            direction_site_indices=sites,
            direction_structure_indices=self.frames[self.offset + positions],
            direction_structure_positions=self.offset + positions,
            direction_indices=plan["slot_indices"][slots],
            image_counts=counts,
        )
        added = sum(value.nbytes for value in columns.values()) + packed_images.size * 4
        self._check(self.rows.nbytes + self.images.nbytes + added)
        self.rows.append(columns)
        self.images.append({"image_vectors": packed_images.astype(np.int32)})
        self.status[self.offset + positions, sites] = 1
        self.offset += n_structures

    def finalize(self):
        result = self.metadata
        for name in self.rows._specifications:
            if name != "image_counts":
                result[name] = self.rows.concatenate(name)
        result["origins"] = puw.standardize(puw.quantity(result["origins"], "nm"))
        result["units"]["origins"] = str(puw.get_unit(result["origins"]))
        result["image_vectors"] = self.images.concatenate("image_vectors")
        counts = self.rows.concatenate("image_counts")
        result["image_offsets"] = np.concatenate(
            (np.zeros(1, dtype=np.int64), np.cumsum(counts))
        )
        result["status"] = self.status
        self.rows.clear()
        self.images.clear()
        return result
