from devtools.scripts import audit_numba_oracle_map as audit


def test_every_current_cpu_kernel_has_one_complete_mapping():
    manifest, errors = audit.build_manifest()

    assert errors == []
    assert manifest["summary"]["cpu_kernels"] == 108
    assert len({entry["kernel_id"] for entry in manifest["kernels"]}) == 108
    assert set(entry["mapping"] for entry in manifest["kernels"]) == {
        "direct",
        "alias",
        "absorbed",
    }


def test_each_used_family_has_consumers_parity_and_independent_evidence():
    manifest, errors = audit.build_manifest()

    assert errors == []
    assert sum(
        contract["kernel_count"]
        for contract in manifest["families"].values()
    ) == manifest["summary"]["cpu_kernels"]
    for contract in manifest["families"].values():
        assert contract["kernel_count"] > 0
        assert contract["consumers"]
        assert contract["parity_tests"]
        assert contract["independent_evidence"]


def test_nested_helper_is_classified_as_absorbed_not_falsely_direct():
    manifest, _ = audit.build_manifest()
    by_id = {entry["kernel_id"]: entry for entry in manifest["kernels"]}
    key = (
        "molsysmt/lib/structure/neighbor_list.py::"
        "_neighbor_csr_multi_pbc::lazy_njit"
    )

    assert by_id[key] == {
        "kernel_id": key,
        "family": "neighbors",
        "mapping": "absorbed",
        "rust_target": (
            "molsysmt._private.rust_backend.neighbor_list_csr_multi"
        ),
    }
