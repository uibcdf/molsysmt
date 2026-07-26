from devtools.scripts import audit_rust_numba_divergences as audit


def test_every_parity_closeness_check_declares_both_tolerances():
    manifest, errors = audit.build_manifest()

    assert errors == []
    assert manifest["summary"]["closeness_sites"] > 0
    assert all(
        site["rtol"] >= 0.0 and site["atol"] >= 0.0
        for site in manifest["closeness_sites"]
    )


def test_every_oracle_parity_file_has_an_accepted_policy():
    manifest, errors = audit.build_manifest()

    assert errors == []
    assert manifest["summary"]["parity_files"] == 14
    assert manifest["provisional"] == []
    assert all(
        policy["status"] == "accepted"
        for policy in manifest["parity_policies"].values()
    )


def test_deliberate_divergences_have_executable_and_independent_evidence():
    manifest, errors = audit.build_manifest()

    assert errors == []
    assert manifest["summary"]["deliberate_divergences"] == 8
    for contract in manifest["deliberate_divergences"]:
        assert contract["status"] == "accepted"
        assert contract["decision"]
        assert contract["tolerance"]
        assert contract["tests"]
        assert contract["evidence"]


def test_must_match_contracts_remain_explicit():
    manifest, errors = audit.build_manifest()

    assert errors == []
    assert manifest["summary"]["must_match_contracts"] == 4
    assert {contract["id"] for contract in manifest["must_match"]} == {
        "orthogonal-pbc-exact",
        "half-box-rounding-exact",
        "integer-series-topology-exact",
        "neighbor-membership-exact",
    }
