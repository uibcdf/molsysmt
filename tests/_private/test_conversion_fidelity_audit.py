"""Testing the generated Tier 1 conversion-fidelity ratchet."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[2]
    / "devtools"
    / "scripts"
    / "audit_conversion_fidelity.py"
)


def _load_audit_module():
    spec = spec_from_file_location("audit_conversion_fidelity", SCRIPT_PATH)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_tier1_conversion_fidelity_audit_has_no_regressions():
    audit = _load_audit_module().build_audit()

    assert audit["scope"] == "direct Tier 1-to-Tier 1 registered conversions"
    assert audit["summary"]["tier1_forms"] > 0
    assert audit["summary"]["direct_edges"] == len(audit["edges"])
    assert not any(audit["violations"].values())


def test_compact_fidelity_baseline_roundtrips_current_debt():
    module = _load_audit_module()
    forms, edges = module._direct_tier1_edges()
    payload = module._baseline_payload(forms, edges)

    assert module._decode_masks(payload) == module._edge_pairs(edges)


def test_generated_matrix_never_calls_scoped_coverage_exhaustive():
    edges = _load_audit_module().build_audit()["edges"]

    for edge in edges:
        if edge["coverage"] == "scoped_preflight":
            assert edge["audited_scopes"] != ["all"]
            assert edge["audited_scopes"]
            assert edge["is_exhaustive"] is False


def test_identity_edges_require_explicit_execution_evidence():
    edges = _load_audit_module().build_audit()["edges"]

    for edge in edges:
        if edge["source"] == edge["target"]:
            assert edge["coverage"] == "scoped_preflight"
            assert edge["audited_scopes"] == ["representation"]
            assert edge["is_exhaustive"] is False
            assert edge["possible_outcomes"] == ["exact", "rejected"]


def test_evidence_backed_native_declarative_routes_are_exhaustive():
    edges = {
        (edge["source"], edge["target"]): edge
        for edge in _load_audit_module().build_audit()["edges"]
    }
    routes = {
        ('molsysmt.MolSys', 'molsysmt.MolSysDict'),
        ('molsysmt.Structures', 'molsysmt.StructuresDict'),
        ('molsysmt.Topology', 'molsysmt.TopologyDict'),
    }

    for route in routes:
        assert edges[route]["coverage"] == "exhaustive_preflight"
        assert edges[route]["audited_scopes"] == ["all"]
        assert edges[route]["is_exhaustive"] is True
