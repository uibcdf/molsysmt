"""
Private helpers for the engine='MolSysMT' branches of add_missing_heavy_atoms
and add_missing_terminal_cappings.

Public API (internal use only):
  - load_residue_template(group_name)
  - place_missing_in_group(topo, all_coords_nm, group_idx, missing_names, template)
  - append_atoms_to_molsys(native_molsys, new_atom_info, new_bonds_info)
  - place_ace_group(N_pos, CA_pos, C_pos, template, n_structures)
  - place_nme_group(C_pos, CA_pos, N_pos_last, template, n_structures)
  - rebuild_molsys_with_new_groups(native_molsys, ...)
"""

from __future__ import annotations
import json
import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Template loader
# ---------------------------------------------------------------------------

_template_cache: dict = {}


def load_residue_template(group_name: str) -> dict | None:
    """Return the residue template dict for *group_name*, or None if absent."""
    if group_name in _template_cache:
        return _template_cache[group_name]
    try:
        from importlib.resources import files
        data = files("molsysmt.data.databases.residue_templates").joinpath(f"{group_name}.json")
        template = json.loads(data.read_text())
    except Exception:
        template = None
    _template_cache[group_name] = template
    return template


# ---------------------------------------------------------------------------
# Bonds sort utility (works on any DataFrame, not only Bonds_DataFrame)
# ---------------------------------------------------------------------------

def _sort_bonds_inplace(bonds_df):
    """Sort bond pairs so atom1_index <= atom2_index, then sort by (atom1, atom2)."""
    mask = bonds_df["atom1_index"] > bonds_df["atom2_index"]
    bonds_df.loc[mask, ["atom1_index", "atom2_index"]] = (
        bonds_df.loc[mask, ["atom2_index", "atom1_index"]].values
    )
    bonds_df.sort_values(by=["atom1_index", "atom2_index"], inplace=True)
    bonds_df.reset_index(drop=True, inplace=True)


# ---------------------------------------------------------------------------
# Kabsch placement of missing atoms within an existing group
# ---------------------------------------------------------------------------

def place_missing_in_group(topo, all_coords_nm, group_idx, missing_names, template):
    """Compute coordinates for *missing_names* in *group_idx* via Kabsch alignment.

    Parameters
    ----------
    topo : Topology
    all_coords_nm : ndarray, shape (n_structures, n_atoms, 3)
    group_idx : int
    missing_names : list[str]
    template : dict

    Returns
    -------
    dict  {atom_name: ndarray(n_structures, 3)}
    """
    from molsysmt.lib.structure.get_least_rmsd_rotation_and_translation import (
        get_least_rmsd_rotation_and_translation_single_structure,
    )

    template_atoms = template["atoms"]
    template_coords = np.asarray(template["coords_nm"], dtype=np.float64)
    template_name_to_idx = {n: i for i, n in enumerate(template_atoms)}

    # Atoms currently present in this group
    group_mask = topo.atoms["group_index"] == group_idx
    existing_rows = topo.atoms[group_mask]
    existing_atom_indices = existing_rows.index.tolist()
    existing_atom_names = existing_rows["atom_name"].tolist()

    # Anchor pairs: atoms present in both structure and template
    common = [
        (aidx, template_name_to_idx[aname])
        for aidx, aname in zip(existing_atom_indices, existing_atom_names)
        if aname in template_name_to_idx
    ]
    if not common:
        return {}

    struct_idxs  = [c[0] for c in common]
    tmpl_idxs    = [c[1] for c in common]
    P_template   = template_coords[tmpl_idxs].astype(np.float64)   # (k, 3)

    n_structures = all_coords_nm.shape[0]
    result = {}

    for missing_name in missing_names:
        if missing_name not in template_name_to_idx:
            continue
        t_pos = template_coords[template_name_to_idx[missing_name]]   # (3,)
        atom_coords = np.empty((n_structures, 3), dtype=np.float64)

        for frame in range(n_structures):
            P_struct = all_coords_nm[frame, struct_idxs, :].astype(np.float64)   # (k, 3)
            # kernel(coordinates=mobile, reference_coordinates=reference)
            # We want to map template → structure, so template=mobile, struct=reference
            center_rot, rotation, translation = \
                get_least_rmsd_rotation_and_translation_single_structure(P_template, P_struct)
            # new_pos = R @ (t_pos - c_mob) + c_mob + t = R @ (t_pos - c_tmpl) + c_struct
            atom_coords[frame] = rotation @ (t_pos - center_rot) + center_rot + translation

        result[missing_name] = atom_coords

    return result


# ---------------------------------------------------------------------------
# Append atoms to an existing native MolSys (no group-index changes)
# ---------------------------------------------------------------------------

def append_atoms_to_molsys(native_molsys, new_atom_info, new_bonds_info):
    """Return a new MolSys with extra atoms appended after the existing ones.

    Parameters
    ----------
    native_molsys : molsysmt.MolSys
    new_atom_info : list of (group_idx, atom_name, coords_array(n_structures, 3))
    new_bonds_info : list of (new_atom_idx1, new_atom_idx2)

    Returns
    -------
    molsysmt.MolSys
    """
    from molsysmt.native import MolSys, Topology
    from molsysmt.native.topology import Bonds_DataFrame
    from molsysmt.element.atom import get_atom_type_from_atom_name
    from molsysmt import pyunitwizard as puw

    topo    = native_molsys.topology
    structs = native_molsys.structures
    n_orig  = topo.n_atoms

    all_coords = puw.get_value(structs.coordinates, to_unit="nm")   # (n_s, n_a, 3)
    n_structures = all_coords.shape[0]

    # --- Build new atom rows ---
    new_rows       = []
    new_coords_list = []

    for group_idx, atom_name, atom_coords in new_atom_info:
        new_atom_idx = n_orig + len(new_rows)
        group_mask = topo.atoms["group_index"] == group_idx
        first_row  = topo.atoms[group_mask].iloc[0]
        comp_idx   = first_row["component_index"]
        chain_idx  = first_row["chain_index"]

        new_rows.append({
            "atom_id":        str(new_atom_idx),
            "atom_name":      atom_name,
            "atom_type":      get_atom_type_from_atom_name(atom_name),
            "group_index":    group_idx,
            "component_index": comp_idx,
            "chain_index":    chain_idx,
        })
        new_coords_list.append(atom_coords)

    # --- Build new topology ---
    new_topo = Topology(skip_digestion=True)

    new_atoms = pd.concat(
        [topo.atoms, pd.DataFrame(new_rows)],
        ignore_index=True,
    )
    new_atoms["group_index"]     = new_atoms["group_index"].astype("Int64")
    new_atoms["component_index"] = new_atoms["component_index"].astype("Int64")
    new_atoms["chain_index"]     = new_atoms["chain_index"].astype("Int64")
    new_atoms["atom_id"]         = new_atoms["atom_id"].astype("string")
    new_topo.atoms     = new_atoms
    new_topo.groups    = topo.groups.copy()
    new_topo.components = topo.components.copy()
    new_topo.molecules  = topo.molecules.copy()
    new_topo.entities   = topo.entities.copy()
    new_topo.chains     = topo.chains.copy()

    # Remap bonds (existing bonds are unchanged; new bonds use absolute new indices)
    bonds_copy = topo.bonds.copy()
    if new_bonds_info:
        extra = Bonds_DataFrame(n_bonds=len(new_bonds_info))
        for k, (i1, i2) in enumerate(new_bonds_info):
            extra.loc[k, "atom1_index"] = int(i1)
            extra.loc[k, "atom2_index"] = int(i2)
        new_bonds = pd.concat([bonds_copy, extra], ignore_index=True)
        new_bonds["atom1_index"] = new_bonds["atom1_index"].astype("Int64")
        new_bonds["atom2_index"] = new_bonds["atom2_index"].astype("Int64")
        _sort_bonds_inplace(new_bonds)
        new_topo.bonds = new_bonds
    else:
        new_topo.bonds = bonds_copy

    # --- Build new coordinates ---
    if new_coords_list:
        extra_coords = np.stack(new_coords_list, axis=1)        # (n_s, n_new, 3)
        new_all_coords = np.concatenate([all_coords, extra_coords], axis=1)
    else:
        new_all_coords = all_coords.copy()

    # --- Assemble new MolSys ---
    new_molsys = MolSys()
    new_molsys.topology  = new_topo
    new_molsys.structures = structs.copy()
    new_molsys.structures.coordinates = puw.quantity(new_all_coords, "nm")

    return new_molsys


# ---------------------------------------------------------------------------
# Geometric placement helpers
# ---------------------------------------------------------------------------

def _normalize(v):
    n = np.linalg.norm(v)
    return v / n if n > 1e-12 else None


def _perpendicular_component(vec, axis):
    """Component of *vec* perpendicular to *axis* (unit vector)."""
    return vec - np.dot(vec, axis) * axis


def place_ace_group(N_pos, CA_pos, C_pos, template, n_structures):
    """Place an ACE capping group at the N-terminus of a residue.

    Parameters
    ----------
    N_pos, CA_pos, C_pos : ndarray(n_structures, 3) – positions of N, CA, C of the first residue
    template : dict  – ACE template
    n_structures : int

    Returns
    -------
    dict  {atom_name: ndarray(n_structures, 3)}
    """
    template_atoms  = template["atoms"]
    template_coords = np.asarray(template["coords_nm"], dtype=np.float64)
    tname2idx = {n: i for i, n in enumerate(template_atoms)}

    # Bond lengths from template
    r_C_O   = float(np.linalg.norm(
        template_coords[tname2idx["C"]] - template_coords[tname2idx["O"]]
    ))
    r_C_CH3 = float(np.linalg.norm(
        template_coords[tname2idx["C"]] - template_coords[tname2idx["CH3"]]
    ))

    result = {name: np.empty((n_structures, 3), dtype=np.float64) for name in template_atoms}

    for frame in range(n_structures):
        N    = N_pos[frame]
        CA   = CA_pos[frame]
        C_res = C_pos[frame]

        v_NCA = _normalize(CA - N)
        if v_NCA is None:
            for name in template_atoms:
                result[name][frame] = N
            continue

        # Perpendicular component of C_res relative to N-CA axis
        C_perp = _normalize(_perpendicular_component(C_res - N, v_NCA))
        if C_perp is None:
            fallback = np.array([1.0, 0.0, 0.0]) if abs(v_NCA[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
            C_perp = _normalize(_perpendicular_component(fallback, v_NCA))

        # Trans omega: C_ACE anti to C_res → use -C_perp
        # Angle C(ACE)−N−CA = 121°
        angle = np.deg2rad(121.0)
        v_N_to_CACE = np.cos(angle) * v_NCA + np.sin(angle) * (-C_perp)
        C_ACE = N + 0.133 * v_N_to_CACE

        # Sp2 plane at C_ACE: defined by C_ACE, N_res0, CA_res0
        v_CN      = _normalize(N - C_ACE)          # C_ACE → N direction
        n_plane   = _normalize(np.cross(N - C_ACE, CA - C_ACE))
        if n_plane is None or v_CN is None:
            for name in template_atoms:
                result[name][frame] = C_ACE
            continue

        # In-plane direction perpendicular to C_ACE→N, pointing toward CA
        v_perp = _normalize(np.cross(n_plane, v_CN))
        if v_perp is None:
            v_perp = np.array([0.0, 1.0, 0.0])

        # O: 120° from N, cis to CA (same side as v_perp)
        # CH3: 120° from N, trans to CA (anti v_perp)
        cos120 = np.cos(np.deg2rad(120.0))
        sin120 = np.sin(np.deg2rad(120.0))
        v_O   = cos120 * v_CN + sin120 * v_perp
        v_CH3 = cos120 * v_CN - sin120 * v_perp

        result["C"][frame]   = C_ACE
        result["O"][frame]   = C_ACE + r_C_O   * v_O
        result["CH3"][frame] = C_ACE + r_C_CH3 * v_CH3

    return result


def place_nme_group(C_pos, CA_pos, N_pos_last, template, n_structures):
    """Place an NME capping group at the C-terminus of a residue.

    Parameters
    ----------
    C_pos, CA_pos, N_pos_last : ndarray(n_structures, 3) – C, CA, N of the last residue
    template : dict  – NME template
    n_structures : int

    Returns
    -------
    dict  {atom_name: ndarray(n_structures, 3)}
    """
    template_atoms  = template["atoms"]
    template_coords = np.asarray(template["coords_nm"], dtype=np.float64)
    tname2idx = {n: i for i, n in enumerate(template_atoms)}

    # NME bond length N-C from template
    r_NC = float(np.linalg.norm(
        template_coords[tname2idx["N"]] - template_coords[tname2idx["C"]]
    ))

    result = {name: np.empty((n_structures, 3), dtype=np.float64) for name in template_atoms}

    for frame in range(n_structures):
        C     = C_pos[frame]
        CA    = CA_pos[frame]
        N_last = N_pos_last[frame]

        v_CAC = _normalize(C - CA)      # CA → C direction
        if v_CAC is None:
            for name in template_atoms:
                result[name][frame] = C
            continue

        # N_last perpendicular to CA→C axis at C
        N_perp = _normalize(_perpendicular_component(N_last - C, v_CAC))
        if N_perp is None:
            fallback = np.array([1.0, 0.0, 0.0]) if abs(v_CAC[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
            N_perp = _normalize(_perpendicular_component(fallback, v_CAC))

        # Trans omega: N_NME anti to N_last → use -N_perp
        # Angle N(NME)−C−CA = 117° (angle between C→N_NME and C→CA)
        # v_CCA = -v_CAC (C toward CA direction)
        v_CCA = -v_CAC
        angle = np.deg2rad(117.0)
        v_C_to_NNME = np.cos(angle) * v_CCA + np.sin(angle) * (-N_perp)
        N_NME = C + 0.133 * v_C_to_NNME

        # C_NME: bonded to N_NME, in the peptide plane, trans to CA
        v_NC    = _normalize(C - N_NME)       # N_NME → C direction
        n_plane = _normalize(np.cross(C - N_NME, CA - N_NME))
        if n_plane is None or v_NC is None:
            result["N"][frame] = N_NME
            result["C"][frame] = N_NME + r_NC * np.array([0.0, 0.0, 1.0])
            continue

        v_perp = _normalize(np.cross(n_plane, v_NC))
        if v_perp is None:
            v_perp = np.array([0.0, 1.0, 0.0])

        # C_NME at 120° from C_last, trans to CA (same side as v_perp by construction)
        cos120 = np.cos(np.deg2rad(120.0))
        sin120 = np.sin(np.deg2rad(120.0))
        v_CNME = cos120 * v_NC + sin120 * v_perp
        C_NME  = N_NME + r_NC * v_CNME

        result["N"][frame] = N_NME
        result["C"][frame] = C_NME

    return result


# ---------------------------------------------------------------------------
# Full topology rebuild — used when new groups are inserted
# ---------------------------------------------------------------------------

def rebuild_molsys_with_new_groups(
    native_molsys,
    mol_group_ranges,
    extra_groups_before,
    extra_groups_after,
):
    """Rebuild a MolSys inserting ACE/NME groups at the correct positions.

    Parameters
    ----------
    native_molsys : molsysmt.MolSys
    mol_group_ranges : dict {mol_idx: (first_group_idx, last_group_idx)}
    extra_groups_before : dict {mol_idx: (group_name, {atom_name: coords(n_s, 3)})}
    extra_groups_after  : dict {mol_idx: (group_name, {atom_name: coords(n_s, 3)})}

    Returns
    -------
    molsysmt.MolSys
    """
    from molsysmt.native import MolSys, Topology
    from molsysmt.native.topology import Bonds_DataFrame
    from molsysmt.element.atom import get_atom_type_from_atom_name
    from molsysmt import pyunitwizard as puw

    topo    = native_molsys.topology
    structs = native_molsys.structures
    n_structures = structs.n_structures

    all_coords = puw.get_value(structs.coordinates, to_unit="nm")   # (n_s, n_orig, 3)

    # group_idx → molecule_idx (via group → molecule_index in groups DataFrame)
    group_to_mol = {}
    for g in range(topo.n_groups):
        mol_idx = topo.groups.loc[g, "molecule_index"] if g < len(topo.groups) else pd.NA
        group_to_mol[g] = mol_idx

    first_group_of_mol = {m: fg for m, (fg, _) in mol_group_ranges.items()}
    last_group_of_mol  = {m: lg for m, (_, lg) in mol_group_ranges.items()}

    # Running lists for the new topology
    new_atom_rows   = []     # list of dicts
    new_atom_coords = []     # list of ndarray(n_structures, 3)
    old_to_new_atom = {}     # old_atom_idx → new_atom_idx

    new_group_rows         = []   # list of dicts
    new_group_to_old_group = {}   # new_g → old_g (or None for inserted)
    new_group_mol          = []   # new_g → mol_idx

    def _add_group_from_dict(group_name, group_id, group_type, atoms_dict, comp_idx, chain_idx, mol_idx):
        """Append an entirely new group (ACE or NME) from a name→coords dict."""
        new_g = len(new_group_rows)
        for atom_name, atom_coords_arr in atoms_dict.items():
            new_idx = len(new_atom_rows)
            new_atom_rows.append({
                "atom_id":         str(new_idx),
                "atom_name":       atom_name,
                "atom_type":       get_atom_type_from_atom_name(atom_name),
                "group_index":     new_g,
                "component_index": comp_idx,
                "chain_index":     chain_idx,
            })
            new_atom_coords.append(atom_coords_arr)   # (n_structures, 3)
        new_group_rows.append({
            "group_id":    str(group_id),
            "group_name":  group_name,
            "group_type":  group_type if group_type else pd.NA,
        })
        new_group_to_old_group[new_g] = None
        new_group_mol.append(mol_idx)

    for g in range(topo.n_groups):
        mol_idx = group_to_mol.get(g, pd.NA)

        # Insert ACE before the first group of this molecule
        if mol_idx is not pd.NA and mol_idx in extra_groups_before:
            if first_group_of_mol.get(mol_idx) == g:
                cap_name, cap_atoms = extra_groups_before[mol_idx]
                gmask     = topo.atoms["group_index"] == g
                first_row = topo.atoms[gmask].iloc[0]
                chain_idx = first_row["chain_index"]
                comp_idx  = first_row["component_index"]
                _add_group_from_dict(cap_name, str(len(new_group_rows)), "terminal capping",
                                     cap_atoms, comp_idx, chain_idx, mol_idx)

        # Add the original group
        orig_g_new = len(new_group_rows)
        gmask = topo.atoms["group_index"] == g
        orig_rows = topo.atoms[gmask]
        orig_idxs = orig_rows.index.tolist()
        chain_idx = orig_rows.iloc[0]["chain_index"] if len(orig_rows) > 0 else pd.NA

        for old_idx in orig_idxs:
            new_idx = len(new_atom_rows)
            old_to_new_atom[int(old_idx)] = new_idx
            row = topo.atoms.iloc[int(old_idx)].to_dict()
            row["group_index"] = orig_g_new
            new_atom_rows.append(row)
            new_atom_coords.append(all_coords[:, int(old_idx), :])   # (n_structures, 3)

        grow = topo.groups.iloc[g].to_dict()
        grow.pop("molecule_index", None)   # will be re-added below
        new_group_rows.append(grow)
        new_group_to_old_group[orig_g_new] = g
        new_group_mol.append(mol_idx)

        # Append NME after the last group of this molecule
        if mol_idx is not pd.NA and mol_idx in extra_groups_after:
            if last_group_of_mol.get(mol_idx) == g:
                cap_name, cap_atoms = extra_groups_after[mol_idx]
                gmask     = topo.atoms["group_index"] == g
                last_row  = topo.atoms[gmask].iloc[-1]
                chain_idx = last_row["chain_index"]
                comp_idx  = last_row["component_index"]
                _add_group_from_dict(cap_name, str(len(new_group_rows)), "terminal capping",
                                     cap_atoms, comp_idx, chain_idx, mol_idx)

    n_new_atoms  = len(new_atom_rows)
    n_new_groups = len(new_group_rows)

    # --- Atoms DataFrame ---
    atoms_df = pd.DataFrame(new_atom_rows)
    atoms_df["group_index"]     = atoms_df["group_index"].astype("Int64")
    atoms_df["component_index"] = atoms_df["component_index"].astype("Int64")
    atoms_df["chain_index"]     = atoms_df["chain_index"].astype("Int64")
    atoms_df["atom_id"]         = atoms_df["atom_id"].astype("string")

    # --- Groups DataFrame (re-attach molecule_index) ---
    old_group_mol = topo.groups["molecule_index"].to_dict()
    mol_col = []
    for new_g in range(n_new_groups):
        old_g = new_group_to_old_group.get(new_g)
        if old_g is not None:
            mol_col.append(old_group_mol.get(old_g, pd.NA))
        else:
            # Inserted cap: molecule_index is already tracked in new_group_mol
            m = new_group_mol[new_g]
            mol_col.append(m if m is not pd.NA else pd.NA)
    groups_df = pd.DataFrame(new_group_rows, index=range(n_new_groups))
    groups_df["molecule_index"] = pd.array(mol_col, dtype="Int64")
    groups_df["group_id"]       = groups_df["group_id"].astype("string")

    # --- Remap existing bonds ---
    new_bonds_rows = []
    for _, brow in topo.bonds.iterrows():
        o1 = int(brow["atom1_index"])
        o2 = int(brow["atom2_index"])
        if o1 in old_to_new_atom and o2 in old_to_new_atom:
            new_bonds_rows.append({
                "atom1_index": old_to_new_atom[o1],
                "atom2_index": old_to_new_atom[o2],
                "order": brow.get("order", pd.NA),
                "type":  brow.get("type", pd.NA),
            })

    # --- Peptide bonds for inserted groups ---
    # Build name→idx lookup per new group
    def _name_to_idx_for_group(new_g):
        mask = atoms_df["group_index"] == new_g
        rows = atoms_df[mask]
        return dict(zip(rows["atom_name"], rows.index.tolist()))

    for new_g in range(n_new_groups):
        if new_group_to_old_group.get(new_g) is not None:
            continue   # original group
        cap_name = new_group_rows[new_g]["group_name"]
        cap_n2i  = _name_to_idx_for_group(new_g)

        # Intra-group bonds from template
        tmpl = load_residue_template(cap_name)
        if tmpl:
            for b1, b2 in tmpl["bonds"]:
                if b1 in cap_n2i and b2 in cap_n2i:
                    new_bonds_rows.append({
                        "atom1_index": cap_n2i[b1],
                        "atom2_index": cap_n2i[b2],
                        "order": pd.NA, "type": pd.NA,
                    })

        # Inter-group peptide bond
        if cap_name == "ACE" and new_g + 1 < n_new_groups:
            next_n2i = _name_to_idx_for_group(new_g + 1)
            if "C" in cap_n2i and "N" in next_n2i:
                new_bonds_rows.append({
                    "atom1_index": cap_n2i["C"],
                    "atom2_index": next_n2i["N"],
                    "order": pd.NA, "type": pd.NA,
                })
        elif cap_name == "NME" and new_g - 1 >= 0:
            prev_n2i = _name_to_idx_for_group(new_g - 1)
            if "C" in prev_n2i and "N" in cap_n2i:
                new_bonds_rows.append({
                    "atom1_index": prev_n2i["C"],
                    "atom2_index": cap_n2i["N"],
                    "order": pd.NA, "type": pd.NA,
                })

    # Build bonds DataFrame
    bonds_df = pd.DataFrame(new_bonds_rows) if new_bonds_rows else Bonds_DataFrame(n_bonds=0)
    if new_bonds_rows:
        bonds_df["atom1_index"] = bonds_df["atom1_index"].astype("Int64")
        bonds_df["atom2_index"] = bonds_df["atom2_index"].astype("Int64")
        _sort_bonds_inplace(bonds_df)

    # --- Coordinates ---
    new_coords = np.stack(new_atom_coords, axis=1)   # (n_structures, n_new_atoms, 3)

    # --- Assemble Topology ---
    new_topo = Topology(skip_digestion=True)
    new_topo.atoms      = atoms_df
    new_topo.groups     = groups_df
    new_topo.components = topo.components.copy()
    new_topo.molecules  = topo.molecules.copy()
    new_topo.entities   = topo.entities.copy()
    new_topo.chains     = topo.chains.copy()
    new_topo.bonds      = bonds_df

    # --- Assemble MolSys ---
    new_molsys = MolSys()
    new_molsys.topology   = new_topo
    new_molsys.structures = structs.copy()
    new_molsys.structures.coordinates = puw.quantity(new_coords, "nm")

    return new_molsys
