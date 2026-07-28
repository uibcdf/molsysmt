#!/usr/bin/env python
"""Building and validating the final CPU Numba-to-Rust oracle map."""
from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from devtools.scripts.audit_numba_surface import collect_inventory  # noqa: E402


MANIFEST = REPO / "devtools" / "data" / "numba_cpu_oracle_map.json"
SCHEMA = "molsysmt.numba-cpu-oracle-map@1"


FAMILY_CONTRACTS = {
    "math": {
        "source_paths": ["molsysmt/lib/math.py"],
        "consumers": [
            "molsysmt/_private/rust_backend.py",
            "molsysmt/build/build_peptide.py",
        ],
        "parity_tests": ["tests/rust/test_math_parity.py"],
        "independent_evidence": ["rust/src/mathlib.rs"],
    },
    "pbc": {
        "source_prefixes": ["molsysmt/lib/pbc/"],
        "consumers": [
            "molsysmt/pbc",
            "molsysmt/form/molsysmt_PDBFileHandler/to_molsysmt_MolSys.py",
        ],
        "parity_tests": ["tests/rust/test_pbc_parity.py"],
        "independent_evidence": [
            "tests/scientific_truth/pbc/test_box_geometry.py",
            "tests/scientific_truth/pbc/test_wrapping.py",
        ],
    },
    "series": {
        "source_paths": ["molsysmt/lib/series.py"],
        "consumers": ["molsysmt/native/topology.py"],
        "parity_tests": ["tests/rust/test_long_tail_parity.py"],
        "independent_evidence": ["rust/src/series.rs"],
    },
    "topology": {
        "source_prefixes": ["molsysmt/lib/topology/"],
        "consumers": [
            "molsysmt/native/_topology_infer.py",
            "molsysmt/element/component/get_component_index.py",
        ],
        "parity_tests": ["tests/rust/test_long_tail_parity.py"],
        "independent_evidence": [
            "tests/scientific_truth/topology/test_graph_topology.py",
            "rust/src/topology.rs",
        ],
    },
    "geometry": {
        "source_paths": [
            "molsysmt/lib/structure/flip.py",
            "molsysmt/lib/structure/get_center.py",
            "molsysmt/lib/structure/get_radius_of_gyration.py",
            "molsysmt/lib/structure/get_rmsf.py",
        ],
        "consumers": [
            "molsysmt/structure/flip.py",
            "molsysmt/structure/get_center.py",
            "molsysmt/structure/get_radius_of_gyration.py",
            "molsysmt/structure/get_rmsf.py",
        ],
        "parity_tests": ["tests/rust/test_long_tail_parity.py"],
        "independent_evidence": [
            "tests/scientific_truth/structure/test_ensemble_observables.py",
            "tests/scientific_truth/structure/test_structural_transformations.py",
        ],
    },
    "distances": {
        "source_paths": ["molsysmt/lib/structure/get_distances.py"],
        "consumers": ["molsysmt/structure/get_distances.py"],
        "parity_tests": ["tests/rust/test_distances_parity.py"],
        "independent_evidence": [
            "tests/scientific_truth/external/mdanalysis/test_geometry.py",
            "tests/scientific_truth/structure/test_pair_reductions.py",
        ],
    },
    "mic_distances": {
        "source_paths": ["molsysmt/lib/structure/get_mic_distances.py"],
        "consumers": ["molsysmt/structure/get_distances.py"],
        "parity_tests": ["tests/rust/test_mic_distances_parity.py"],
        "independent_evidence": [
            "tests/scientific_truth/pbc/test_minimum_image.py",
            "tests/rust/test_mic_neighbors_battery.py",
        ],
    },
    "neighbors": {
        "source_paths": ["molsysmt/lib/structure/neighbor_list.py"],
        "consumers": [
            "molsysmt/structure/get_contacts.py",
            "molsysmt/structure/get_neighbors.py",
        ],
        "parity_tests": ["tests/rust/test_neighbor_list_parity.py"],
        "independent_evidence": [
            "tests/scientific_truth/structure/test_pair_reductions.py",
            "tests/rust/test_mic_neighbors_battery.py",
        ],
    },
    "sasa": {
        "source_paths": ["molsysmt/lib/structure/get_sasa.py"],
        "consumers": ["molsysmt/physchem/get_sasa.py"],
        "parity_tests": [
            "tests/rust/test_sasa_cell_list_parity.py",
            "tests/rust/test_min_distance_and_bruteforce_sasa_parity.py",
        ],
        "independent_evidence": ["rust/src/sasa.rs"],
    },
    "angles": {
        "source_paths": [
            "molsysmt/lib/structure/get_angles.py",
            "molsysmt/lib/structure/get_mic_angles.py",
        ],
        "consumers": ["molsysmt/structure/get_angles.py"],
        "parity_tests": ["tests/rust/test_angles_parity.py"],
        "independent_evidence": [
            "tests/scientific_truth/external/mdanalysis/test_geometry.py",
            "rust/src/angles.rs",
        ],
    },
    "dihedrals": {
        "source_paths": [
            "molsysmt/lib/structure/get_dihedral_angles.py",
            "molsysmt/lib/structure/get_mic_dihedral_angles.py",
        ],
        "consumers": ["molsysmt/structure/get_dihedral_angles.py"],
        "parity_tests": ["tests/rust/test_dihedrals_parity.py"],
        "independent_evidence": [
            "tests/scientific_truth/external/mdtraj/test_geometry.py",
            "rust/src/dihedrals.rs",
        ],
    },
    "dihedral_ops": {
        "source_paths": [
            "molsysmt/lib/structure/set_dihedral_angles.py",
            "molsysmt/lib/structure/set_mic_dihedral_angles.py",
            "molsysmt/lib/structure/shift_dihedral_angles.py",
            "molsysmt/lib/structure/shift_mic_dihedral_angles.py",
        ],
        "consumers": ["molsysmt/structure/set_dihedral_angles.py"],
        "parity_tests": ["tests/rust/test_dihedral_ops_parity.py"],
        "independent_evidence": [
            "tests/scientific_truth/structure/test_dihedral_editing.py"
        ],
    },
    "rmsd": {
        "source_paths": [
            "molsysmt/lib/structure/get_rmsd.py",
            "molsysmt/lib/structure/get_least_rmsd.py",
            "molsysmt/lib/structure/get_least_rmsd_rotation_and_translation.py",
        ],
        "consumers": [
            "molsysmt/structure/get_rmsd.py",
            "molsysmt/structure/get_least_rmsd.py",
            "molsysmt/structure/least_rmsd_fit.py",
            "molsysmt/build/_native_placers.py",
        ],
        "parity_tests": ["tests/rust/test_rmsd_parity.py"],
        "independent_evidence": [
            "tests/scientific_truth/external/mdanalysis/test_geometry.py",
            "tests/scientific_truth/curated/pentalanine/test_trajectory.py",
        ],
    },
    "axes": {
        "source_paths": [
            "molsysmt/lib/structure/get_principal_geometric_axes.py",
            "molsysmt/lib/structure/get_principal_inertia_axes.py",
        ],
        "consumers": ["molsysmt/structure/get_principal_axes.py"],
        "parity_tests": ["tests/rust/test_axes_parity.py"],
        "independent_evidence": [
            "tests/scientific_truth/structure/test_principal_axes.py"
        ],
    },
    "pca": {
        "source_paths": [
            "molsysmt/lib/structure/principal_component_analysis.py"
        ],
        "consumers": ["molsysmt/structure/principal_component_analysis.py"],
        "parity_tests": ["tests/rust/test_pca_parity.py"],
        "independent_evidence": [
            "tests/scientific_truth/structure/test_principal_component_analysis.py",
            "rust/src/pca.rs",
        ],
    },
}


ABSORBED_TARGETS = {
    ("molsysmt/lib/math.py", "angle"): "rust-internal:mathlib::angle",
    ("molsysmt/lib/math.py", "cross_product"): "rust-internal:mathlib::cross_product",
    ("molsysmt/lib/math.py", "dihedral_angle"): "rust-internal:mathlib::dihedral_angle",
    ("molsysmt/lib/math.py", "dot_product"): "rust-internal:mathlib::dot_product",
    ("molsysmt/lib/math.py", "norm_vector"): "rust-internal:mathlib::norm_vector",
    (
        "molsysmt/lib/structure/get_distances.py",
        "get_distance_two_points_single_structure",
    ): "rust-internal:distances::dist3",
    (
        "molsysmt/lib/structure/get_mic_distances.py",
        "get_mic_distance_two_points_single_structure",
    ): "rust-internal:mic::mic_distance_auto",
}


def _family_for_path(path: str) -> str | None:
    matches = []
    for family, contract in FAMILY_CONTRACTS.items():
        if path in contract.get("source_paths", ()) or any(
            path.startswith(prefix)
            for prefix in contract.get("source_prefixes", ())
        ):
            matches.append(family)
    return matches[0] if len(matches) == 1 else None


def _rust_backend_functions(root: Path) -> set[str]:
    path = root / "molsysmt" / "_private" / "rust_backend.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _kernel_parts(kernel_id: str) -> tuple[str, str]:
    path, qualified, _decorator = kernel_id.split("::", 2)
    return path, qualified.rsplit(".", 1)[-1]


def _absorbed_target(path: str, function: str, family: str) -> str | None:
    explicit = ABSORBED_TARGETS.get((path, function))
    if explicit is not None:
        return explicit
    if family == "neighbors" and function.startswith(("_", "neighbor_")):
        return "molsysmt._private.rust_backend.neighbor_list_csr_multi"
    if family == "sasa" and function.startswith(("_is_", "_mic_")):
        rust_name = "get_mic_sasa" if "mic" in function else "get_sasa"
        return f"molsysmt._private.rust_backend.{rust_name}"
    return None


def build_manifest(root: Path = REPO) -> tuple[dict, list[str]]:
    """Returning the complete current CPU oracle map and validation errors."""

    errors = []
    inventory = collect_inventory(root)
    backend_functions = _rust_backend_functions(root)
    kernels = []

    for kernel_id in inventory["guarded"]["cpu_jit_sites"]:
        path, function = _kernel_parts(kernel_id)
        family = _family_for_path(path)
        if family is None:
            errors.append(f"{kernel_id}: no unique family")
            continue

        if function in backend_functions:
            kind = "direct"
            target = f"molsysmt._private.rust_backend.{function}"
        elif function == "_jit_serialize" and "jit_serialize" in backend_functions:
            kind = "alias"
            target = "molsysmt._private.rust_backend.jit_serialize"
        else:
            kind = "absorbed"
            target = _absorbed_target(path, function, family)
            if target is None:
                errors.append(f"{kernel_id}: no Rust target")
                continue

        kernels.append(
            {
                "kernel_id": kernel_id,
                "family": family,
                "mapping": kind,
                "rust_target": target,
            }
        )

    families = {}
    used_families = {kernel["family"] for kernel in kernels}
    for family in sorted(used_families):
        contract = {
            key: value
            for key, value in FAMILY_CONTRACTS[family].items()
            if key not in {"source_paths", "source_prefixes"}
        }
        for category in ("consumers", "parity_tests", "independent_evidence"):
            if not contract.get(category):
                errors.append(f"{family}: empty {category}")
            for relative in contract.get(category, ()):
                if not (root / relative).exists():
                    errors.append(f"{family}: missing {category} path {relative}")
        contract["kernel_count"] = sum(
            kernel["family"] == family for kernel in kernels
        )
        families[family] = contract

    expected = set(inventory["guarded"]["cpu_jit_sites"])
    observed = {kernel["kernel_id"] for kernel in kernels}
    for missing in sorted(expected - observed):
        errors.append(f"{missing}: absent from generated map")
    for extra in sorted(observed - expected):
        errors.append(f"{extra}: stale generated map entry")

    output = {
        "schema": SCHEMA,
        "source_inventory_schema": inventory["schema"],
        "summary": {
            "cpu_kernels": len(kernels),
            "families": len(families),
            "direct": sum(kernel["mapping"] == "direct" for kernel in kernels),
            "alias": sum(kernel["mapping"] == "alias" for kernel in kernels),
            "absorbed": sum(kernel["mapping"] == "absorbed" for kernel in kernels),
        },
        "families": families,
        "kernels": kernels,
    }
    return output, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    current, errors = build_manifest()
    if errors:
        print("CPU Numba oracle map FAILED:")
        for error in errors:
            print(f"  - {error}")
        return 1
    if args.json:
        print(json.dumps(current, indent=2, sort_keys=True))
        return 0
    if args.write_manifest:
        MANIFEST.write_text(
            json.dumps(current, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote CPU oracle map: {MANIFEST.relative_to(REPO)}")
        return 0
    if not MANIFEST.exists():
        print("CPU Numba oracle map FAILED: generated manifest is missing")
        return 1
    recorded = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if recorded != current:
        print(
            "CPU Numba oracle map FAILED: manifest is stale; inspect the "
            "generated diff before using --write-manifest"
        )
        return 1

    summary = current["summary"]
    print(
        "CPU Numba oracle map: PASS | "
        f"{summary['cpu_kernels']} kernels | {summary['families']} families | "
        f"{summary['direct']} direct | {summary['alias']} alias | "
        f"{summary['absorbed']} absorbed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
