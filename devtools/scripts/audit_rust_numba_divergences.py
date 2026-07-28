#!/usr/bin/env python
"""Building and validating the final Rust/Numba divergence contract."""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
ORACLE_MAP = REPO / "devtools" / "data" / "numba_cpu_oracle_map.json"
MANIFEST = REPO / "devtools" / "data" / "rust_numba_divergences.json"
SCHEMA = "molsysmt.rust-numba-divergences@1"


PARITY_POLICIES = {
    "tests/rust/test_angles_parity.py": {
        "families": ["angles"],
        "status": "accepted",
        "basis": "Absolute floating-point envelope for vector reductions.",
    },
    "tests/rust/test_axes_parity.py": {
        "families": ["axes"],
        "status": "accepted",
        "basis": (
            "Eigenvalues use an absolute/relative spectral envelope; eigenvectors "
            "are checked up to sign and against the eigen-equation."
        ),
    },
    "tests/rust/test_dihedral_ops_parity.py": {
        "families": ["dihedral_ops"],
        "status": "accepted",
        "basis": (
            "Absolute coordinate envelope after an in-place rotation; the unsafe "
            "Numba broadcast case is checked against Rust with expanded input."
        ),
    },
    "tests/rust/test_dihedrals_parity.py": {
        "families": ["dihedrals"],
        "status": "accepted",
        "basis": "Absolute angular envelope for vector reductions.",
    },
    "tests/rust/test_distances_parity.py": {
        "families": ["distances"],
        "status": "accepted",
        "basis": "Absolute distance envelope with explicit zero relative tolerance.",
    },
    "tests/rust/test_long_tail_parity.py": {
        "families": ["geometry", "series", "topology"],
        "status": "accepted",
        "basis": (
            "Measured fastmath reduction gap for floating outputs; integer outputs "
            "remain exact and empty-input corrections are explicit."
        ),
    },
    "tests/rust/test_math_parity.py": {
        "families": ["math"],
        "status": "accepted",
        "basis": "Tight absolute envelope plus independent algebraic invariants.",
    },
    "tests/rust/test_mic_distances_parity.py": {
        "families": ["mic_distances"],
        "status": "accepted",
        "basis": (
            "Absolute MIC-distance envelope, backed by wide-shell minimum-image "
            "ground truth."
        ),
    },
    "tests/rust/test_min_distance_and_bruteforce_sasa_parity.py": {
        "families": ["math", "sasa"],
        "status": "accepted",
        "basis": (
            "Exact minimum-distance values where applicable and an absolute SASA "
            "envelope for fastmath ordering."
        ),
    },
    "tests/rust/test_neighbor_list_parity.py": {
        "families": ["neighbors"],
        "status": "accepted",
        "basis": (
            "Exact CSR membership and offsets; absolute envelope only for stored "
            "floating distances."
        ),
    },
    "tests/rust/test_pbc_parity.py": {
        "families": ["pbc"],
        "status": "accepted",
        "basis": (
            "Exact orthogonal results and measured 1e-12 absolute FMA envelope for "
            "triclinic arithmetic; corrected MIC behavior uses a property oracle."
        ),
    },
    "tests/rust/test_pca_parity.py": {
        "families": ["pca"],
        "status": "accepted",
        "basis": (
            "Spectral envelope with sign- and degeneracy-aware eigenvector checks "
            "against the independently rebuilt covariance matrix."
        ),
    },
    "tests/rust/test_rmsd_parity.py": {
        "families": ["rmsd"],
        "status": "accepted",
        "basis": (
            "Absolute/relative eigensolver and reduction envelope, plus direct "
            "superposition and proper-rotation properties."
        ),
    },
    "tests/rust/test_sasa_cell_list_parity.py": {
        "families": ["sasa"],
        "status": "accepted",
        "basis": (
            "Absolute SASA envelope and agreement with the independent brute-force "
            "implementation."
        ),
    },
}


DIVERGENCES = [
    {
        "id": "triclinic-minimum-image-correction",
        "families": ["pbc", "mic_distances"],
        "category": "scientific-correction",
        "numba_behavior": (
            "The triclinic helper searches around the unwrapped vector and can return "
            "a non-minimum image for coordinates several cells away."
        ),
        "rust_behavior": (
            "The search is centered on the wrapped candidate and returns the true "
            "minimum image."
        ),
        "decision": "Keep the Rust correction; do not preserve the Numba defect.",
        "tolerance": {"rtol": 0.0, "atol": 1e-12},
        "tests": [
            "tests/rust/test_pbc_parity.py::test_wrap_to_mic_is_minimum_image_on_a_triclinic_box",
            "tests/rust/test_mic_neighbors_battery.py::test_dense_mic_distance_matrix_matches_ground_truth",
        ],
        "evidence": [
            "devguide/pending_bugs/wrap_to_mic_triclinic_not_minimum_image.md",
            "tests/scientific_truth/pbc/test_minimum_image.py",
        ],
        "status": "accepted",
    },
    {
        "id": "triclinic-neighbor-completeness-correction",
        "families": ["neighbors"],
        "category": "scientific-correction",
        "numba_behavior": (
            "The skewed-cell binning and single-image wrap can omit or add neighbor "
            "pairs in triclinic boxes."
        ),
        "rust_behavior": (
            "Neighbor membership matches a wide-shell all-pairs ground truth."
        ),
        "decision": "Keep the complete Rust neighbor set.",
        "tolerance": {"membership": "exact", "distance_atol": 1e-9},
        "tests": [
            "tests/rust/test_neighbor_list_parity.py::test_pbc_self",
            "tests/rust/test_mic_neighbors_battery.py::test_self_neighbour_list_matches_ground_truth",
        ],
        "evidence": [
            "devguide/pending_proposals/triclinic_cell_list_completeness.md"
        ],
        "status": "accepted",
    },
    {
        "id": "sasa-orthogonal-branch-correction",
        "families": ["sasa"],
        "category": "implementation-correction",
        "numba_behavior": (
            "A typo in the orthogonality helper selects the triclinic path for an "
            "orthogonal box."
        ),
        "rust_behavior": "Orthogonal boxes use the intended branch.",
        "decision": "Keep the Rust branch correction.",
        "tolerance": {"rtol": 0.0, "atol": 1e-9},
        "tests": [
            "tests/rust/test_sasa_cell_list_parity.py::test_mic_sasa_cell_list",
            "tests/rust/test_min_distance_and_bruteforce_sasa_parity.py::test_get_mic_sasa_bruteforce",
        ],
        "evidence": [
            "tests/rust/test_mic_neighbors_battery.py::test_cell_list_sasa_equals_brute_force_across_boxes"
        ],
        "status": "accepted",
    },
    {
        "id": "periodic-dihedral-broadcast-correction",
        "families": ["dihedral_ops"],
        "category": "safety-and-contract-correction",
        "numba_behavior": (
            "The periodic multi-structure kernel reads past a size-one structure axis "
            "instead of applying the documented broadcast."
        ),
        "rust_behavior": "The size-one structure axis broadcasts deterministically.",
        "decision": "Honor the public broadcast contract.",
        "tolerance": {"rtol": 0.0, "atol": 1e-12},
        "tests": [
            "tests/rust/test_dihedral_ops_parity.py::test_broadcast_angles_deliberate_divergence_on_the_periodic_path"
        ],
        "evidence": [
            "devguide/pending_bugs/dihedral_angles_broadcast_mismatch_pbc.md"
        ],
        "status": "accepted",
    },
    {
        "id": "empty-series-safety-correction",
        "families": ["series"],
        "category": "safety-and-contract-correction",
        "numba_behavior": (
            "Two helpers read element zero before checking an empty input and can "
            "produce a phantom chunk or unchecked native access."
        ),
        "rust_behavior": "Empty input returns empty, shape-valid outputs.",
        "decision": "Keep the defined empty-input result.",
        "tolerance": {"integer_output": "exact"},
        "tests": [
            "tests/rust/test_long_tail_parity.py::test_empty_series_diverge_because_upstream_reads_out_of_bounds"
        ],
        "evidence": ["rust/src/series.rs"],
        "status": "accepted",
    },
    {
        "id": "principal-axis-sign-canonicalization",
        "families": ["axes"],
        "category": "mathematical-nonuniqueness",
        "numba_behavior": "LAPACK may choose either sign for each eigenvector.",
        "rust_behavior": (
            "The largest-magnitude component is made positive deterministically."
        ),
        "decision": (
            "Canonicalize signs while comparing scientific axes up to sign."
        ),
        "tolerance": {"eigenvalue_rtol": 1e-9, "eigenvalue_atol": 1e-9},
        "tests": [
            "tests/rust/test_axes_parity.py::test_axes_parity",
            "tests/rust/test_axes_parity.py::test_the_rust_sign_convention_is_stable",
        ],
        "evidence": [
            "devguide/pending_bugs/principal_axes_eigenvector_sign_unspecified.md"
        ],
        "status": "accepted",
    },
    {
        "id": "pca-spectral-nonuniqueness",
        "families": ["pca"],
        "category": "mathematical-nonuniqueness",
        "numba_behavior": (
            "Eigenvector signs are arbitrary and a degenerate null space can use any "
            "orthonormal basis."
        ),
        "rust_behavior": (
            "Signs are canonicalized; degenerate bases may differ while satisfying "
            "the same covariance eigenproblem."
        ),
        "decision": (
            "Compare eigenvalues and isolated eigenvectors, and use the eigen-equation "
            "for degenerate subspaces."
        ),
        "tolerance": {"eigenvalue_rtol": 1e-8, "eigenvalue_atol": 1e-8},
        "tests": [
            "tests/rust/test_pca_parity.py::test_rank_deficient_case_agrees_on_eigenvalues_only",
            "tests/rust/test_pca_parity.py::test_the_eigen_equation_holds_for_every_component",
        ],
        "evidence": [
            "tests/scientific_truth/structure/test_principal_component_analysis.py"
        ],
        "status": "accepted",
    },
    {
        "id": "rodrigues-return-normalization",
        "families": ["math"],
        "category": "private-seam-normalization",
        "numba_behavior": "The helper mutates its vector and returns None.",
        "rust_behavior": "The extension returns the rotated vector.",
        "decision": (
            "The private coexistence seam returns the rotated vector for both backends; "
            "the public scientific behavior is unchanged."
        ),
        "tolerance": {"rtol": 0.0, "atol": 1e-14},
        "tests": ["tests/rust/test_math_parity.py::test_rodrigues_rotation"],
        "evidence": ["molsysmt/_private/rust_backend.py"],
        "status": "accepted",
    },
]


MUST_MATCH = [
    {
        "id": "orthogonal-pbc-exact",
        "families": ["pbc"],
        "contract": "Orthogonal wrapping and box classification remain exact.",
        "tests": ["tests/rust/test_pbc_parity.py::test_wrap_kernels_mutate_identically"],
    },
    {
        "id": "half-box-rounding-exact",
        "families": ["pbc"],
        "contract": "Exact half-box jumps use the same ties-to-even convention.",
        "tests": ["tests/rust/test_pbc_parity.py::test_unwrap_agrees_on_exact_half_box_jumps"],
    },
    {
        "id": "integer-series-topology-exact",
        "families": ["series", "topology"],
        "contract": "Integer indices, offsets, and orders remain bit-for-bit equal.",
        "tests": [
            "tests/rust/test_long_tail_parity.py::test_serie_to_chunks_round_trip",
            "tests/rust/test_long_tail_parity.py::test_occurrence_order",
        ],
    },
    {
        "id": "neighbor-membership-exact",
        "families": ["neighbors"],
        "contract": "CSR offsets and neighbor indices remain exact where both oracles are valid.",
        "tests": ["tests/rust/test_neighbor_list_parity.py::test_vacuum_self"],
    },
]


def _module_functions(path: Path) -> dict[str, ast.FunctionDef]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _numeric_constants(tree: ast.Module) -> dict[str, float]:
    output = {}
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        target = node.target if isinstance(node, ast.AnnAssign) else node.targets[0]
        value = node.value
        if (
            isinstance(target, ast.Name)
            and isinstance(value, ast.Constant)
            and isinstance(value.value, (int, float))
        ):
            output[target.id] = float(value.value)
    return output


def _number(node: ast.AST, constants: dict[str, float]) -> float | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.Name):
        return constants.get(node.id)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        value = _number(node.operand, constants)
        return None if value is None else -value
    return None


def _closeness_sites(path: Path, relative: str) -> tuple[list[dict], list[str]]:
    errors = []
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    constants = _numeric_constants(tree)
    output = []
    for function, node in _module_functions(path).items():
        calls = [
            child
            for child in ast.walk(node)
            if isinstance(child, ast.Call)
            and isinstance(child.func, ast.Attribute)
            and child.func.attr in {"allclose", "isclose"}
        ]
        calls.sort(key=lambda child: (child.lineno, child.col_offset))
        for index, call in enumerate(calls, start=1):
            keywords = {keyword.arg: keyword.value for keyword in call.keywords}
            missing = {"rtol", "atol"} - keywords.keys()
            if missing:
                errors.append(
                    f"{relative}::{function}::closeness#{index}: "
                    f"missing explicit {', '.join(sorted(missing))}"
                )
                continue
            rtol = _number(keywords["rtol"], constants)
            atol = _number(keywords["atol"], constants)
            if rtol is None or atol is None:
                errors.append(
                    f"{relative}::{function}::closeness#{index}: "
                    "tolerance is not a module constant or numeric literal"
                )
                continue
            output.append(
                {
                    "site": f"{relative}::{function}::closeness#{index}",
                    "operation": call.func.attr,
                    "rtol": rtol,
                    "atol": atol,
                }
            )
    return output, errors


def _validate_test_reference(reference: str, errors: list[str]) -> None:
    relative, separator, function = reference.partition("::")
    path = REPO / relative
    if not path.exists():
        errors.append(f"missing evidence path: {relative}")
    elif separator and function not in _module_functions(path):
        errors.append(f"missing test function: {reference}")


def build_manifest() -> tuple[dict, list[str]]:
    errors = []
    oracle = json.loads(ORACLE_MAP.read_text(encoding="utf-8"))
    parity_files = sorted(
        {
            path
            for family in oracle["families"].values()
            for path in family["parity_tests"]
        }
    )
    missing_policies = set(parity_files) - PARITY_POLICIES.keys()
    stale_policies = PARITY_POLICIES.keys() - set(parity_files)
    errors.extend(f"missing parity policy: {path}" for path in sorted(missing_policies))
    errors.extend(f"stale parity policy: {path}" for path in sorted(stale_policies))

    closeness_sites = []
    policies = {}
    for relative in parity_files:
        path = REPO / relative
        if not path.exists():
            errors.append(f"missing parity test: {relative}")
            continue
        sites, site_errors = _closeness_sites(path, relative)
        errors.extend(site_errors)
        closeness_sites.extend(sites)
        policy = dict(PARITY_POLICIES[relative])
        policy["closeness_site_count"] = len(sites)
        policies[relative] = policy

    known_families = set(oracle["families"])
    for contract in [*DIVERGENCES, *MUST_MATCH]:
        unknown = set(contract["families"]) - known_families
        if unknown:
            errors.append(
                f"{contract['id']}: unknown families {', '.join(sorted(unknown))}"
            )
        for reference in contract["tests"]:
            _validate_test_reference(reference, errors)
        for reference in contract.get("evidence", ()):
            _validate_test_reference(reference, errors)

    provisional = [
        relative
        for relative, policy in policies.items()
        if policy["status"] != "accepted"
    ] + [
        contract["id"]
        for contract in DIVERGENCES
        if contract["status"] != "accepted"
    ]

    output = {
        "schema": SCHEMA,
        "source_oracle_schema": oracle["schema"],
        "summary": {
            "parity_files": len(parity_files),
            "closeness_sites": len(closeness_sites),
            "deliberate_divergences": len(DIVERGENCES),
            "must_match_contracts": len(MUST_MATCH),
            "provisional": len(provisional),
        },
        "parity_policies": policies,
        "closeness_sites": closeness_sites,
        "deliberate_divergences": DIVERGENCES,
        "must_match": MUST_MATCH,
        "provisional": provisional,
    }
    return output, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--require-closed", action="store_true")
    args = parser.parse_args()

    current, errors = build_manifest()
    if args.require_closed and current["provisional"]:
        errors.append(
            "provisional contracts remain: " + ", ".join(current["provisional"])
        )
    if errors:
        print("Rust/Numba divergence audit FAILED:")
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
        print(f"Wrote divergence manifest: {MANIFEST.relative_to(REPO)}")
        return 0
    if not MANIFEST.exists():
        print("Rust/Numba divergence audit FAILED: manifest is missing")
        return 1
    recorded = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if recorded != current:
        print(
            "Rust/Numba divergence audit FAILED: manifest is stale; inspect the "
            "generated diff before using --write-manifest"
        )
        return 1

    summary = current["summary"]
    print(
        "Rust/Numba divergence audit: PASS | "
        f"{summary['parity_files']} parity files | "
        f"{summary['closeness_sites']} explicit closeness sites | "
        f"{summary['deliberate_divergences']} deliberate divergences | "
        f"{summary['must_match_contracts']} must-match contracts | "
        f"{summary['provisional']} provisional"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
